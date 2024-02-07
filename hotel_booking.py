"""
System Requirements
We'll focus on the following set of requirements while designing the Hotel Management System:

- The system should support the booking of different room types like standard, deluxe, family suite, etc.

- Guests should be able to search room inventory and book any available room.

- The system should be able to retrieve information like who book a particular room or what are the rooms booked by a specific customer.

- The system should allow customers to cancel their booking. Full refund if the cancelation is done before 24 hours of check-in date.


Usecases
Here are the main Actors in our system:
- Guest: All guests can search the available rooms, as well as make a booking.
- Receptionist: Mainly responsible for adding and modifying rooms, creating room bookings, check-in, and check-out customers.
- System: Mainly responsible for sending notifications for room booking, cancellation, etc.
- Manager: Mainly responsible for adding new workers.
- Housekeeper: To add/modify housekeeping record of rooms.
- Server: To add/modify room service record of rooms.
"""

from enum import Enum

class RoomType(Enum):
    STANDARD, DELUXE, FAMILY_SUITE = 1, 2, 3

class RoomStatus(Enum):
    AVAILABLE, NOT_AVAILABLE, RESERVED = 1, 2, 3

class BookingStatus(Enum):
    CONFIRMED, CANCELLED, CHECK_IN, CHECK_OUT = 1, 2, 3, 4

class PaymentStatus(Enum):
    UNPAID, COMPLETED, CANCELLED = 1, 2, 3

class Person:
    def __init__(self, name, address, email, phone, account):
        self._name = name
        self._address = address
        self._email = email
        self._phone = phone
        self._account = account

class Guest(Person):
    def __init__(self, name, address, email, phone, account):
        super().__init__(name, address, email, phone, account)
        self._room = None
    
    def set_room(self, room):
        self._room = room
    
    def get_room(self):
        return self._room
    
    def book_room(self, system, room, check_in_time, check_out_time, price, booking_status, payment_status):
        if room.get_status()==RoomStatus.AVAILABLE:
            system.book_room(self, room, check_in_time, check_out_time, price, booking_status, payment_status)

    def check_out(self, system):
        system.check_out(self)

    def cancel(self, system):
        system.cancel(self)

    def search(self, style, start_date, end_date):
        pass

class Receptionist(Person):
    def __init__(self, name, address, email, phone, account):
        super().__init__(name, address, email, phone, account)

    def search(self):
        pass

class System:
    def __init__(self):
        self._room = []
        self._booking_histories = []
    
    def retrive_room_by_guest(self, guest):
        return guest.get_room()

    def retrive_guest_by_room(self, room):
        return room.get_owner()
    
    def book_room(self, guest, room, check_in_time, check_out_time, price, booking_status, payment_status):
        book_transaction = BookingTransaction(guest,room,check_in_time, check_out_time, price, booking_status, payment_status)
        self._booking_histories.append(book_transaction)

    def find_transaction(self, guest,room, status):
        for transaction in self._booking_histories:
            if transaction.get_guest() == guest and transaction.get_room()==room and transaction.get_booking_status()==status:
                return transaction

    def payment(self, guest, room):
        pass

    def refund(self, guest, room):
        pass

    def check_out(self, guest):
        room = guest.get_room()
        transaction = self.find_transaction(guest, room, BookingStatus.CHECK_IN)
        self.payment(guest, room)
        transaction.set_booking_status(BookingStatus.CHECK_OUT)
        transaction.set_payment_status(PaymentStatus.COMPLETED)
        guest.set_room(None)
        room.set_owner(None)

    def cancel(self, guest):
        room = guest.get_room()
        transaction = self.find_transaction(guest, room)
        self.refund(guest, room)
        transaction.set_booking_status(BookingStatus.CANCELLED)
        transaction.set_payment_status(PaymentStatus.CANCELLED)
        guest.set_room(None)
        room.set_owner(None)
    
            
class BookingTransaction:
    def __init__(self,guest,room, check_in_time, check_out_time, price, booking_status, payment_status):
        self._guest = guest
        self._room = room
        self._check_in_time = check_in_time
        self._check_out_time = check_out_time
        self._booking_status = booking_status
        self._price = price
        self._payment_status = payment_status

        self.room.set_status(RoomStatus.RESERVED)
        self.room.set_owner(guest)
        self.guest.set_room(room)
    
class Room:
    def __init__(self, room_type, status=RoomStatus.AVAILABLE, price, room_number):
        self._room_type = room_type
        self._status = status
        self._price = price
        self._room_number = room_number
        self._owner = None

    def set_owner(self, guest):
        self._owner = guest

    def get_owner(self):
        return self._owner
    
    def set_status(self, status):
        self._status = status



