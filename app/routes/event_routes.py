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


#events user organizer
@router.get("/my-organizer-events", response_model=List[dict])
async def get_all_events_i_organize(current_user: dict = Depends(get_current_user)):
    """
    Get all events where the user is an organizer.
    This means: any participant with role='organizer'.
    """
    db = connection.db

    # Find events where current user appears as organizer in participants
    events = await db["events"].find(
        {
            "participants": {
                "$elemMatch": {
                    "user_id": current_user["user_id"],
                    "role": "organizer"
                }
            }
        }
    ).to_list(length=200)

    return [event_helper(event) for event in events]


#delete only by organizer
@router.delete("/{event_id}", status_code=status.HTTP_200_OK)
async def delete_event(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an event.
    Any organizer (creator or invited organizer) can delete it.
    """
    db = connection.db

    # Validate event ID
    try:
        obj_id = ObjectId(event_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid event ID")

    # Fetch event
    event = await db["events"].find_one({"_id": obj_id})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Get all organizers using your helper
    organizers = await get_organizers(event_id)

    # Check if current user is among organizers
    is_organizer = any(
        organizer.user_id == current_user["user_id"]
        for organizer in organizers
    )

    if not is_organizer:
        raise HTTPException(
            status_code=403,
            detail="Only organizers can delete the event"
        )

    # Delete the event
    await db["events"].delete_one({"_id": obj_id})

    return {"message": "Event deleted successfully"}

#malak 
async def get_organizers(event_id: str) -> List[EventParticipant] | None:
    db = connection.db
    event = await db["events"].find_one({"_id": ObjectId(event_id)})

    # Event not found
    if not event:
        return []

    # Safely get participants list
    participants = event.get("participants", [])

    # Filter organizers
    organizers = [
        EventParticipant(**p)
        for p in participants
        if UserRole(p.get("role")) == UserRole.ORGANIZER
    ]

    return organizers

#organizer can list attendees
@router.get("/{event_id}/attendees")
async def get_event_attendees(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Allow any organizer (creator or invited) to view attendees.
    Uses get_organizers() helper.
    """
    db = connection.db

    # Validate event ID
    try:
        obj_id = ObjectId(event_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid event ID")

    # Fetch event
    event = await db["events"].find_one({"_id": obj_id})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # 🔥 Use your helper
    organizers = await get_organizers(event_id)

    # Check if current user is one of the organizers
    is_organizer = any(
        organizer.user_id == current_user["user_id"]
        for organizer in organizers
    )

    if not is_organizer:
        raise HTTPException(
            status_code=403,
            detail="Only organizers can view attendees"
        )

    # Extract only attendees
    attendees = [
        p for p in event.get("participants", [])
        if p["role"] == "attendee"
    ]

    return {
        "event_id": event_id,
        "title": event["title"],
        "attendees": attendees
    }

#user view events they invited to
@router.get("/invited-events", response_model=List[dict])
async def get_invited_events(current_user: dict = Depends(get_current_user)):
    """
    Users can view all events they are invited to.
    This means any event where the user appears in participants
    (either as attendee or organizer), but is NOT the creator.
    """
    db = connection.db

    events = await db["events"].find(
        {
            "participants": {
                "$elemMatch": {
                    "user_id": current_user["user_id"]
                }
            },
            # Exclude events created by the user (optional)
            "organizer_id": {"$ne": current_user["user_id"]}
        }
    ).to_list(length=200)

    return [event_helper(event) for event in events]

#user list events they're attendance_status is 'Going'.
@router.get("/going", response_model=List[dict])
async def get_events_user_is_going_to(current_user: dict = Depends(get_current_user)):
    """
    Return all events where the user is a participant
    AND their attendance_status is 'Going'.
    """
    db = connection.db

    events = await db["events"].find(
        {
            "participants": {
                "$elemMatch": {
                    "user_id": current_user["user_id"],
                    "attendance_status": "Going"
                }
            }
        }
    ).to_list(length=200)

    return [event_helper(event) for event in events]
