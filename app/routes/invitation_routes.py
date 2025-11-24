from fastapi import APIRouter, HTTPException
from ..models.user import User
from ..models.event import Event
from ..routes.event_routes import get_organizers
from ..email_templates.InvitationTemplate import InvitationTemplate
from ..email_templates.EmailService import EmailService
from ..models.event import EventParticipant
from ..database import connection
from bson import ObjectId



router = APIRouter()


@router.post("/{event_id}/attendee/{email}")
async def invite_attendee(user_id: str, event_id: str, email: str, user_role: str = "attendee"):
    """
    Invite an attendee to an event via email.
    """
    # Implementation for inviting an attendee goes here
    db = connection.db
    event = await db["events"].find_one({"_id": ObjectId(event_id)})
    organizers = await get_organizers(event["_id"])
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    flag = False
    for organizer in organizers:
        if(organizer.email == user["email"]):
            flag = True
            break
    if not flag:
        raise HTTPException(status_code=403, detail="Only organizers can invite attendees.")
    participants = event.get("participants", [])

    for participant in participants:
        if participant["email"] == email:
            raise HTTPException(status_code=400, detail="User is already invited.")
    
    new_user = await db["users"].find_one({"email": email})
    new_participant = EventParticipant(
        user_id= str(new_user["_id"]),
        username= new_user["username"],
        email= email,
        role= user_role,
        attendance_status= "Pending"
    )
    # Here you would typically update the event in the database to add the new participant
    updated_participants = await db["events"].update_one(
        {"_id": event["_id"]},
        {"$push": {"participants": new_participant.model_dump()}}
    )

    if(updated_participants.modified_count == 0):
        raise HTTPException(status_code=404, detail="Event not found")

    # Send invitation email
    template = InvitationTemplate()
    email_service = EmailService(template)
    if( user_role == "organizer"):
        context = {"name": new_user["username"], "app_name": "Event planner System", "role": "organizer","event_name": event["title"]}
    else:
        context = {"name": new_user["username"], "app_name": "Event planner System", "role": "attendee","event_name": event["title"]}
    email_service.send_email(email, context)


    return {"message": "Invitation sent successfully."}


