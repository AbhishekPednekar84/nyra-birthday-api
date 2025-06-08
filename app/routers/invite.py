import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from ..database.models import PartyInvitees
from ..database.db import SessionDep
from sqlmodel import select
from typing import List
from pydantic import BaseModel
from ..dependencies.security import create_jwt_token, verify_jwt_token
from datetime import datetime


router = APIRouter()


class RSVPConfirmRequest(BaseModel):
    invitee_identifier: uuid.UUID


@router.get("/invitees_all", status_code=status.HTTP_200_OK)
def get_all_products(session: SessionDep) -> List[PartyInvitees]:
    return session.exec(select(PartyInvitees)).all()


@router.post("/invitees", status_code=status.HTTP_201_CREATED)
def create_invitee(party_invitee: PartyInvitees, session: SessionDep) -> PartyInvitees:
    if not party_invitee.name or not party_invitee.mobile_number:
        raise HTTPException(
            status_code=400, detail="Name and/or mobile number are required"
        )

    invitee_data = session.exec(
        select(PartyInvitees).where(
            PartyInvitees.mobile_number == party_invitee.mobile_number
        )
    ).first()

    if invitee_data:
        raise HTTPException(
            status_code=400, detail="Invitee with this mobile number already exists"
        )

    session.add(party_invitee)
    session.commit()
    session.refresh(party_invitee)
    return party_invitee


@router.get("/invitees", status_code=status.HTTP_200_OK)
def get_invitee_details(
    session: SessionDep,
    invitee_identifier: uuid.UUID | None,
):
    if not invitee_identifier:
        raise HTTPException(status_code=400, detail="Required details are missing")

    invitee = session.exec(
        select(PartyInvitees).where(
            PartyInvitees.invitee_identifier == invitee_identifier,
        )
    ).first()

    if not invitee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invitee not found"
        )

    token_payload = {"sub": str(invitee.invitee_identifier), "scope": "invitee"}

    jwt = create_jwt_token(token_payload)

    return {"invitee": invitee, "token": jwt}


@router.put("/invitees", status_code=status.HTTP_201_CREATED)
async def update_invite_rsvp(
    invitee: RSVPConfirmRequest,
    session: SessionDep,
    _invitee_identifier: str = Depends(verify_jwt_token),
) -> PartyInvitees:
    invitee_data = session.exec(
        select(PartyInvitees).where(
            PartyInvitees.invitee_identifier == invitee.invitee_identifier
        )
    ).first()

    now = datetime.utcnow()

    print(_invitee_identifier)

    if not invitee_data:
        raise HTTPException(status_code=404, detail="Invitee not found")

    if str(invitee.invitee_identifier) != _invitee_identifier:
        raise HTTPException(status_code=403, detail="Token does not match invitee")

    invitee_data.rsvp = True
    invitee_data.rsvp_date = now

    session.add(invitee_data)
    session.commit()
    session.refresh(invitee_data)
    return {
        "invitee_identifier": invitee_data.invitee_identifier,
        "rsvp_status": invitee_data.rsvp,
    }
