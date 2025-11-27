from ..models.event import EventSearchParams
from ..core.security import get_current_user
from ..database import connection
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
router = APIRouter()

@router.post("/search", response_model=List[dict])
async def advanced_search_events(
    search_params: EventSearchParams,
    current_user: dict = Depends(get_current_user)
):
 
    db = connection.db
    
    query = {
        "participants.user_id": current_user["user_id"]
    }
    
    
    # 1. by event name -> case-insensitive partial match
    if search_params.event_name:
        query["title"] = {
            "$regex": search_params.event_name,
            "$options": "i"  #insensitive
        }
    
    # 2. by date -> partial match
    if search_params.date:
        query["date"] = {
            "$regex": search_params.date,
            "$options": "i"
    
        }
    # 3. by description -> case-insensitive partial match
    if search_params.description:
        query["description"] = {
            "$regex": search_params.description,
            "$options": "i"
        }
    
    # 4. by location -> case-insensitive partial match
    if search_params.location:
        query["location"] = {
            "$regex": search_params.location,
            "$options": "i"
        }
    
    # 5. by role in the event
    if search_params.user_role and search_params.user_role.lower() != "all":
        query["participants"] = {
            "$elemMatch": {
                "user_id": current_user["user_id"],
                "role": search_params.user_role.lower()
            }
        }
    
    
    try:
        events = await db["events"].find(query).to_list(length=200)
        
        # Filter results based on complex role/attendance logic (client-side filtering)
        filtered_events = []
        for event in events:
            for participant in event.get("participants", []):
                if participant["user_id"] == current_user["user_id"]:
                    # Apply role filter if specified
                    if search_params.user_role and search_params.user_role.lower() != "all":
                        if participant["role"] != search_params.user_role.lower():
                            break
                    
                    filtered_events.append(event)
                    break
        
        return [event_helper(event) for event in filtered_events]
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )
        
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
