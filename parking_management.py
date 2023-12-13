"""
1. The parking lot should have multiple floors where customers can park their cars
2. Customers can collect a parking ticket from the entry points and can pay the parking fee at the exit points on their way out.
3. The system should support a per-hour parking fee model. For example, customers have to pay $4 for the first hour, $3.5 for the second and third hours, and $2.5 for all the remaining hours.
4. The system should not allow more vehicles than the maximum capacity of each floor of the parking lot.
"""
from datetime import datetime
import random 
class Constant: 
    def __init__(self):
        self.FEE_PER_HOUR = 5

class Account:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
    
class Customer(Account):
    def __init__(self, id, username, email, password):
        super().__init__(id, username, email, password)    
        self.list_cars = {}

    def add_car(self, car):
        self.list_cars[len(self.list_cars)+1] = car

    def create_ticket(self, parking_floor, car_id):
        if parking_floor.is_full():
            print("This parking floor does not have any available slot. Try other floors")
            return None
        
        available_slot = parking_floor.get_available_slot()
        ticket = Ticket(self.id, car_id, parking_floor.id, available_slot)
        ticket.update_start_time()
        parking_floor.update_slot(available_slot, True)
        print("Ticket is created")
        return ticket

    def pay_ticket(self, ticket):
        pass
    
    def exit_parking(self, ticket, parking_floor):
        ticket.update_end_time()
        ticket.calculate_fee()
        self.pay_ticket(ticket)
        parking_floor.update_slot(ticket.index_slot, False)
        print("Payment successfully, open the gate")

class Ticket:
    def __init__(self, customer_id, car_id, parking_floor_id, index_slot):
        self.customer_id = customer_id
        self.car_id =car_id
        self.parking_floor_id = parking_floor_id
        self.index_slot = index_slot
        self.fee = 0
        self.start_time = 0
        self.end_time = 0

    def update_start_time(self):
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def update_end_time(self):
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def calculate_fee(self):
        time_difference = self.end_time - self.start_time
        hours = time_difference.total_seconds() / 3600
        self.fee = hours * Constant.FEE_PER_HOUR

class Car:
    def __init__(self, model, type, userID):
        self.model = model
        self.type = type
        self.owned_by = userID
        self.id = None

    def update_id(self,id):
        self.id = id
    
class ParkingFloor:
    def __init__(self, max_slot):
        self.id = None
        self.current_slot = 0
        self.max_slot = max_slot
        self.slot = [True for _ in range(max_slot)]

    def update_slot(self, index, value):
        self.slot[index] = value
        if value ==True:
            self.current_slot +=1
        else:
            self.current_slot -=1

    def get_available_slot(self):
        available_slots = [index for index in range(len(self.slot)) if self.slot[index]==True]
        return random.choice(available_slots)

    def update_id(self, id):
        self.id = id
    
    def is_full(self):
        if self.current_slot == self.max_slot:
            return True
        return False
    
class ParkingLot:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.parking_floors = {}
    
    def add_parking_floor(self, parking_floor):
        self.parking_floors[len(self.parking_floors)+1] = parking_floor