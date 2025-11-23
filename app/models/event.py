from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class AttendanceStatus(str, Enum):
    GOING = "Going"
    MAYBE = "Maybe"
    NOT_GOING = "Not Going"
    PENDING = "Pending"

class UserRole(str, Enum):
    ORGANIZER = "organizer"
    ATTENDEE = "attendee"

class EventParticipant(BaseModel):
    user_id: str
    username: str
    email: str
    role: UserRole
    attendance_status: AttendanceStatus = AttendanceStatus.PENDING

class Event(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    location: str = Field(..., min_length=3, max_length=200)
    organizer_id: Optional[str] = None  # Set automatically from token
    participants: List[EventParticipant] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class EventCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    location: str = Field(..., min_length=3, max_length=200)
    invited_emails: List[str] = []  # Emails of people to invite

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = Field(None, min_length=3, max_length=200)

class AttendanceUpdate(BaseModel):
    attendance_status: AttendanceStatus