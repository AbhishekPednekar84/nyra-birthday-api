import uuid
import dotenv

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from pydantic import EmailStr
from datetime import datetime

dotenv.load_dotenv()

TODAY = date.today().strftime("%d-%b-%Y")


class PartyInvitees(SQLModel, table=True):
    __tablename__ = "party_invitees"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    callout_name: str
    mobile_number: str
    gender: str
    invitee_identifier: uuid.UUID = Field(default_factory=uuid.uuid4, index=True)
    email_address: Optional[EmailStr] = Field(default=None)
    rsvp: bool = Field(default=False)
    rsvp_date: Optional[datetime] = Field(default=None)
    child: bool = Field(default=False)
    invite_sent: bool = Field(default=False)
