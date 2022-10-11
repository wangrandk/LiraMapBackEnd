from datetime import datetime
import json
from math import sqrt, pow, acos, pi
from random import betavariate
from re import T
from typing import List
# from sqlalchemy.orm import Session

from sqlalchemy.sql import select

from databases.core import Connection
from lira_backend_api.core.models import (
    DRDMeasurement,
    MeasurementTypes,
    MeasurementModel,
    Trip,
    Device,
    SourceType,
    MapReference,
)
from lira_backend_api.core.schemas import boundary

async def get_measurementtype(measurement_type_id: str, db: Connection):

    query = select(MeasurementTypes).where(MeasurementTypes.id == measurement_type_id)
    result = await db.fetch_one(query)

    result = MeasurementTypes(id=result._mapping["MeasurementTypeId"], created_date=result._mapping["Created_Date"], type=result._mapping["type"])
    
    return result


def get_measurementmodel(measurement_model_id: str, db: Connection):

    return (
        db.query(MeasurementModel)
        .filter(MeasurementModel.id == measurement_model_id)
        .first()
    )


def get_drdmeasurement(drdmeasurement_id: str, db: Connection):

    return (
        db.query(DRDMeasurement).filter(DRDMeasurement.id == drdmeasurement_id).first()
    )


def get_mapreference(mapreference_id: str, db: Connection):
    return db.query(MapReference).filter(MapReference.id == mapreference_id).first()


def get_trip(trip_id: str, db: Connection):
    # We need to swallow the value error, but one could argue that Pydantic should be failing first
    result = db.query(Trip).filter(Trip.id == trip_id).first()

    return result


def get_deviceid(device_id: str, db: Connection):
    return db.query(Device).filter(Device.id == device_id).first()


def get_sourcetype(source_id: str, db: Connection):
    return db.query(SourceType).filter(SourceType.id == source_id).first()


def convert_date(json_created_date: any):
    str_format_date = json_created_date[:-6]
    str_format_date = str_format_date.split(".")[0]
    date_as_iso = datetime.fromisoformat(str_format_date)
    return date_as_iso

def get_ride(trip_id: str, tag: str, db: Connection):
    tripList = list()
    values = list()
    res = (
        db.query(
            MeasurementModel.message,
            MeasurementModel.lat,
            MeasurementModel.lon,
            MeasurementModel.created_date,
        )
        .where(MeasurementModel.fk_trip == trip_id)
        .filter(
            MeasurementModel.tag == tag
            and MeasurementModel.lon != None
            and MeasurementModel.lat != None
        )
        .order_by(MeasurementModel.created_date)
        .limit(500)
        .all()
    )
    #print(res)
    res1 = json.loads(res[0][0])
    val = res1.get(f"{tag}.value")
    if val is None:
        return None

    for x in res:
        jsonobj = json.loads(x[0])
        try:
            if jsonobj.get(f"{tag}.value") is not None:
                value = int(jsonobj.get(f"{tag}.value"))
                values.append(value)
                json_created_date = jsonobj.get("Created_Date")
            else:
                pass
            if json_created_date is not None:
                date_as_iso = convert_date(json_created_date)
                tripList.append(
                    {
                        "trip_id": trip_id,
                        "lat": x[1],
                        "lng": x[2],
                        "value": value,
                        "metadata": date_as_iso,
                    }
                )
            else:
                json_created_date = jsonobj.get("@ts")
                date_as_iso = convert_date(json_created_date)
                tripList.append(
                    {
                        "trip_id": trip_id,
                        "lat": x[1],
                        "lng": x[2],
                        "value": value,
                        "metadata": date_as_iso,
                    }
                )

        except Exception as e:
            print(e)
            value = None

    minX = min(tripList, key=lambda x: x["metadata"])
    maxX = max(tripList, key=lambda x: x["metadata"])
    minY = min(values)
    maxY = max(values)

    return {"path": tripList, "bounds": boundary(minX, maxX, minY, maxY)}


def get_trips(db: Connection):
    rides = (
        db.query(Trip)
        .where(Trip.task_id != 0)
        .filter(Trip.start_position_lat != None)
        .filter(Trip.start_position_lng != None)
        .filter(Trip.end_position_lat != None)
        .filter(Trip.end_position_lng != None)
        .order_by(Trip.task_id)
        .limit(150)
        .all()
    )
    return rides

def get_current_acceleration(trip_id: str,db: Connection):
    acc_vector = list()
    res = db.query(
                MeasurementModel.message 
                ).where(
                    MeasurementModel.fk_trip == trip_id,
                    MeasurementModel.tag == 'acc.xyz'
                ).order_by(MeasurementModel.created_date).limit(100).all()
    for i in res:
        jsonobj = json.loads(i[0])
        if jsonobj.get("acc.xyz.x") and jsonobj.get("acc.xyz.y") and jsonobj.get("acc.xyz.z")  is not None:
            x = jsonobj.get("acc.xyz.x") #xyz-vector based on data from the database.
            y = jsonobj.get("acc.xyz.y") #What the reference frame is, is unclear. Need to ask in class. 
            z = jsonobj.get("acc.xyz.z") #Eg. in which direction does the reference frame of x, y & z point.
            #Length is used to calculate the direction. It is also called the magnitude of the vector.
            #Hence it is the relative acceleration wrt. the xyz frame.
            length = sqrt(pow(x,2) + pow(y,2) + pow(z,2)) 
            alpha = acos(x/length) * 180/pi #Angle(in degrees) of xyz-vector wrt. x-axis
            beta = acos(y/length) * 180/pi #Angle of xyz-vector wrt. y-axis
            gamma = acos(z/length) * 180/pi #Angle of xyz-vector wrt. z-axis
            #Assuming created date is at least not None.
            json_created_date = jsonobj.get("@ts") 
            created_date = convert_date(json_created_date)
            direction = list()
            direction.append( #The 3d xyz-vector is pointing in a direction in each dimension.
                    {
                        "alpha": alpha, 
                        "beta": beta, 
                        "gamma": gamma, 
                    })
            acceleration.append(
                    {
                        "x": x,
                        "y": y,
                        "z": z,
                        "length": length,
                        "direction": direction,
                        "created_date": created_date,
                    })
        else:
            acceleration.append(
                {
                    "x": None,
                    "y": None,
                    "z": None,
                    "length": None,
                    "direction": None,
                    "created_date": None,
                }
            )
    return {"acceleration": acceleration}
