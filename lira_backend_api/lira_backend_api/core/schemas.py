from typing import Any, List, Union

from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from datetime import datetime
from sqlalchemy import BigInteger
from collections import namedtuple

@dataclass
class MeasurementTypes():
    id: UUID
    # type: str
    created_date: datetime
    # MeasurementTypeId: UUID = Field(alias="id")
    type: str
    # created_date: datetime
    # Created_Date: datetime = Field(alias="created_date")
    # class Config:
        # allow_population_by_field_name = True
        # orm_mode = True

@dataclass
class MeasurementModel():
    id: UUID
    timestamp: datetime
    tag: Union[str, None]
    lat: Union[float, None]
    lon: Union[float, None]
    message: Union[str, None]
    is_computed: Union[bool, None]
    fk_trip: Union[UUID, None]
    fk_measurement_type: Union[UUID, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]

    #class Config:
        #orm_mode = True
        #allow_population_by_field_name = True

@dataclass
class Device():
    id: UUID
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]
    fk_sourcetype: Union[UUID, None]

    class Config:
        orm_mode = True

@dataclass
class Trip():
    id: UUID
    task_id: int
    start_time_utc: Union[datetime,None]
    end_time_utc: Union[datetime,None]
    start_position_lat: Union[str,None]
    start_position_lng: Union[str,None]
    start_position_display: Union[str,None]
    end_position_lat: Union[str,None]
    end_position_lng: Union[str,None]
    end_position_display: Union[str,None]
    duration: Union[datetime,None]
    distance_km: Union[float,None]
    fk_device: Union[UUID,None]
    created_date: Union[datetime,None]
    updated_date: Union[datetime,None]
    fully_imported: Union[bool,None]
    #fully_route_annotated: Union[bool,None]
    #description: Union[str,None]
    #change_log: Union[str,None]

    # class Config:
    #     orm_mode = True
    #allow_population_by_field_name = True

@dataclass
class SourceType():
    id: UUID
    source_name: Union[str, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]

    class Config:
        orm_mode = True


class TripTest(BaseModel):
    trip_id: Union[str, None]
    lat: Union[float, None]
    lng: Union[float, None]
    value: Union[int, None]
    metadata: Any

    class Config:
        orm_mode = True

@dataclass
class DRDMeasurement():

    id: UUID
    distance: str
    tag: Union[str, None]
    lat: Union[float, None]
    lon: Union[float, None]
    message: Union[str, None]
    is_computed: Union[bool, None]
    fk_trip: Union[UUID, None]
    fk_measurement_type: Union[UUID, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]

    class Config:
        orm_mode = True


boundary = namedtuple("Boundary", ["minX", "maxX", "minY", "maxY"])


class TripsReturn(BaseModel):
    path: List[TripTest]
    bounds: boundary
    start_city: str
    end_city: str

    class Config:
        orm_mode = True

@dataclass
class MapReference(BaseModel):

    id: str
    lat_MapMatched: Union[float,None]
    lon_MapMatched: Union[float,None]
    way_point_name: Union[str,None]
    leg_summary_map_matched: Union[str,None]
    leg_distance_map_matched: Union[float,None]
    node_id_map_matched: Union[str,None]
    offset: Union[str,None]
    lane: Union[str,None]
    direction: Union[str,None]
    possible_matching_routes: Union[str,None]
    way_point: Union[str,None]
    fk_measurement_id: Union[str,None]
    fk_osmwaypointid: Union[int,None]

    class Config:
        orm_mode = True

class ContentDirection(BaseModel):
    alpha: Union[float,None] #Angle of xyz-vector with respect to x-axis
    beta: Union[float,None] #Angle of xyz-vector with respect to y-axis
    gamma: Union[float,None] #Angle of xyz-vector with respect to z-axis

    class Config:
        orm_mode = True

class ContentAcceleration(BaseModel):
    x: Union[float,None]
    y: Union[float,None]
    z: Union[float,None]
    length: Union[float,None]
    direction: List[ContentDirection]
    created_date: Union[datetime, None]

    class Config:
        orm_mode = True


class Acceleration(BaseModel):
    acceleration: List[ContentAcceleration]
    
    class Config:
        orm_mode = True
