from fastapi import APIRouter, Depends, HTTPException

# from sqlalchemy.orm import Session
from databases.core import Connection

from lira_backend_api.core.schemas import MapReference
from lira_backend_api.v1.routers.utils import get_mapreference
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/mapreference")


# Migrated over
@router.get("/id/{mapreference_id}", response_model=MapReference)
async def get_mapreference_id(
    mapreference_id: str, db: Connection = Depends(get_connection)
):
    result = await get_mapreference(mapreference_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="No values for mapreference id")

    result_dict = dict(result._mapping.items())

    # This could result in a serialization error for testing; we might want to put this into a helper function,
    # or something since we've got several models and schemas to work with
    return MapReference(*result_dict.values())
