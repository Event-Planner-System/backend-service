from fastapi import APIRouter, HTTPException, Depends, status
from ..models.event import EventCreate, EventParticipant, UserRole, AttendanceStatus
from ..core.security import get_current_user
from ..database import connection
from datetime import datetime
from bson import ObjectId
from typing import List

router = APIRouter()

# Helper function to convert ObjectId to string
def event_helper(event) -> dict:
    return {
        "id": str(event["_id"]),
        "title": event["title"],
        "description": event.get("description"),
        "date": event["date"],
        "time": event["time"],
        "location": event["location"],
        "organizer_id": event["organizer_id"],
        "participants": event.get("participants", []),
        "created_at": event.get("created_at"),
        "updated_at": event.get("updated_at")
    }


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new event. The creator automatically becomes the organizer.
    """
    db = connection.db
    
    # Create organizer participant (the creator)
    organizer = EventParticipant(
        user_id=current_user["user_id"],
        username=current_user["username"],
        email=current_user["email"],
        role=UserRole.ORGANIZER,
        attendance_status=AttendanceStatus.GOING
    )
    
    participants = [organizer.model_dump()]
    
    # Add invited attendees (excluding the organizer's email)
    if event_data.invited_emails:
        for email in event_data.invited_emails:
            # Skip if the email is the organizer's email
            if email.lower() == current_user["email"].lower():
                continue
                
            # Find user by email
            invited_user = await db["users"].find_one({"email": email})
            if invited_user:
                # Make sure we don't add the organizer again
                if str(invited_user["_id"]) == current_user["user_id"]:
                    continue
                    
                attendee = EventParticipant(
                    user_id=str(invited_user["_id"]),
                    username=invited_user["username"],
                    email=invited_user["email"],
                    role=UserRole.ATTENDEE,
                    attendance_status=AttendanceStatus.PENDING
                )
                participants.append(attendee.model_dump())
    
    # Create event document
    event_dict = {
        "title": event_data.title,
        "description": event_data.description,
        "date": event_data.date,
        "time": event_data.time,
        "location": event_data.location,
        "organizer_id": current_user["user_id"],
        "participants": participants,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    # Insert event into database
    result = await db["events"].insert_one(event_dict)
    
    # Fetch the created event
    created_event = await db["events"].find_one({"_id": result.inserted_id})
    
    return {
        "message": "Event created successfully",
        "event": event_helper(created_event)
    }


@router.get("/my-events", response_model=List[dict])
async def get_my_organized_events(current_user: dict = Depends(get_current_user)):
    """
    Get all events organized by the current user.
    """
    db = connection.db
    
    events = await db["events"].find(
        {"organizer_id": current_user["user_id"]}
    ).to_list(length=100)
    
    return [event_helper(event) for event in events]


@router.delete("/{event_id}", status_code=status.HTTP_200_OK)
async def delete_event(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an event. Only the organizer who created it can delete the event.
    """
    db = connection.db
    
    try:
        event = await db["events"].find_one({"_id": ObjectId(event_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid event ID")
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if current user is the organizer
    if event["organizer_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="Only the organizer can delete this event"
        )
    
    # Delete the event
    await db["events"].delete_one({"_id": ObjectId(event_id)})
    
    return {"message": "Event deleted successfully"}