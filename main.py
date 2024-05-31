"""
Have these endpoints:

GET / -> list[airline_name]
GET /:airline_name -> list[flight_num]
GET /:airline_name/:flight_num -> Flight

POST /:airline
PUT /:airline/:flight_num
DELETE /:airline/:flight_num

"""
import json
from fastapi import FastAPI
from models import Flight, Airline

app = FastAPI()


with open("airlines.json", "r") as f:
    airline_dict = json.load(f)


airlines: dict[str, list[Flight]] = {}


for airline_name_str, flights_data in airline_dict.items():
    
    airline_flights = []
    for flight_json in flights_data:
        flight_num = flight_json["flight_num"]
        capacity = flight_json["capacity"]
        estimated_flight_duration = flight_json["estimated_flight_duration"]
        
        flight = Flight(flight_number=flight_num, capacity=capacity, estimated_flight_duration=estimated_flight_duration)
        airline_flights.append(flight)

        airline_name = airline_name_str
        airlines[airline_name] = Airline(name=airline_name, flights= airline_flights)
   

@app.get("/")
async def list_airlines() -> list:
    return airlines.keys()

@app.get("/{airline_name}")
async def flight_numbers(airline_name: str) -> list:
    return [flight.flight_number for flight in airlines[airline_name].flights]

@app.get("/{airline_name}/{flight_number}")
async def print_flight(airline_name: str, flight_number: str):
    for flight in airlines[airline_name].flights:
        if flight.flight_number == flight_number:
            return flight 
        
@app.post("/{airline_name}")
async def add_flight(airline_name: str):
    return airlines[airline_name].flights.append(flight)

@app.put("/{airline_name}/{flight_number}")
async def update_flight(airline_name: str, flight_number: str, updated_flight: Flight):
    flights = airlines[airline_name].flights
    for i, flight in enumerate(flights):
        if flight.flight_number == flight_number:
            flights[i] = updated_flight
            return "Flight updated succesfully"
    flights.append(updated_flight)
    return "Flight created succesfully"

@app.delete("/{airline_name}/{flight_number}")
async def delete_flight(airline_name: str, flight_number: str):
    flights = airlines[airline_name].flights
    for flight in flights:
        if flight.flight_number == flight_number:
            flights.remove(flight)
            return "Flight deleted succsefully"

    
    



