"""
Ways to approach a general Design problem.

    Use Cases Generation: Gather all the possible use cases

    Constraints and Analysis: How many users, how much data etc.

    Basic Design: Most basic design. Few users case.

    Bottlenecks: Find the bottlenecks and solve them.

    Scalability: A large number of users. 4 and 5 step will go in loop till we get a satisfactory answer

Current Scenario

    1. Use cases for this problem.
    Parking can be single-level or multilevel.
    Types of vehicles that can be parked, separate spaces for each type of vehicle.
    Entry and exit points.
    2. Constraints
    Number of vehicles that can be accommodated of any type.
    3. Basic Design/High-Level Components
    Vehicle/Type of vehicle.
    Entry and Exit points.
    Different spots for vehicles.
    4. Bottlenecks
    Capacity breach for any type of vehicle.
    5. Scalability
    Scalable from single-level to multi-level
    Scalable from Bike only parking to accommodate all kinds of vehicles.
"""

from enum import Enum
from abc import abstractmethod, ABC
from datetime import datetime
class ParkingStatus(Enum):
    EMPTY, OCCUPIED = 0, 1

class TypeOfSlot(Enum):
    BIKE, MOTORBIKE, CAR = 0, 1, 2

class TypeOfVehicle(Enum):
    BIKE, MOTORBIKE, CAR = 0, 1, 2

class Parking:
    def __init__(self, parking_id, floors, parking_name, address):
        self._parking_id = parking_id
        self._floors = floors
        self._parking_name = parking_name
        self._address = address

class Floor:
    def __init__(self, floor_id, floor_number, parking_slots):
        self._floor_id = floor_id
        self._floor_number = floor_number
        self._parking_slots = parking_slots

class ParkingSlot:
    def __init__(self, slot_id, slot_number, status, type_slot):
        self._slot_id = slot_id
        self._slot_number =slot_number
        self._status = status
        self._type_slot = type_slot
        self._vehicle = None

    def park_vehicle(self,vehicle):
        if (vehicle.get_type()==self._type_slot):
            self._vehicle = vehicle
            self._status = ParkingStatus.OCCUPIED
        else:
            print("This parking slot is not possible for this vehicle type")
    
class Vehicle(ABC):
    @abstractmethod
    def get_type(self):
        pass

class Bike(Vehicle):
    def __init__(self, bike_number):
        self._bike_number = bike_number
    
    def get_type(self):
        return TypeOfVehicle.BIKE
    
class MotorBike(Vehicle):
    def __init__(self, motorbike_number):
        self.motorbike_number = motorbike_number
    
    def get_type(self):
        return TypeOfVehicle.MOTORBIKE

class Car(Vehicle):
    def __init__(self, car_number):
        self.car_number = car_number
    
    def get_type(self):
        return TypeOfVehicle.CAR
    
class TicketController:
    def __init__(self):
        self._vehicle_tickets = {}

    def check_in(self,vehicle, parking):
        self._vehicle_tickets[vehicle] = ParkingTicket(vehicle, parking)

    def check_out(self, vehicle):
        ticket = self._vehicle_tickets[vehicle]
        ticket.exit_time = datetime.now()
        return ticket
    
class ParkingTicket:
    def __init__(self, vehicle, parking):
        self.vehicle = vehicle
        self.parking_slot = parking
        self.entry_time = datetime.now()
        self.exit_time = None