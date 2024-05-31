from pydantic import BaseModel


class Flight(BaseModel):
    flight_number: str
    capacity: int
    estimated_flight_duration: int

class Airline(BaseModel):
    name: str
    flights: list[Flight] 

