from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Response, Depends, HTTPException
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import Trip
from lira_backend_api.v1.routers.utils import get_trip, get_trips
from lira_backend_api.database.db import get_db

router = APIRouter(prefix='/trips')

@router.get("/id/{trip_id}", response_model=Trip)
def get_single_trip(trip_id: UUID, db: Session = Depends(get_db)):
    result = get_trip(str(trip_id), db)

    if result is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    return result

@router.get("", response_model=List[Trip])
def get_all_trips(db: Session = Depends(get_db)):
    results = get_trips(db)

    return results
