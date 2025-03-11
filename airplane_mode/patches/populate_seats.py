import frappe
import random

def execute():
    """
    Patch to populate the 'seat' field in existing Airplane Ticket documents
    using the defined seat allocation logic.
    """
    # Fetch all Airplane Ticket records where seat is not set
    tickets = frappe.get_all("Airplane Ticket", filters={"seat": ["is", "not set"]}, fields=["name"])

    # Get a set of all existing seats
    existing_seats = get_existing_seats()

    for ticket in tickets:
        # Assign a seat using the logic
        seat = generate_unique_seat(existing_seats)

        if seat:
            # Update the seat field
            frappe.db.set_value("Airplane Ticket", ticket.name, "seat", seat)

    frappe.db.commit()  # Ensure changes are committed

def generate_unique_seat(existing_seats):
    """
    Generates a unique seat number ensuring no duplicates exist.
    """
    while True:
        row = random.randint(1, 50)  # Rows from 1 to 50
        seat_letter = random.choice(["A", "B", "C", "D", "E"])  # Seat letters
        seat = f"{row}{seat_letter}"

        if seat not in existing_seats:
            existing_seats.add(seat)  # Mark this seat as taken
            return seat

def get_existing_seats():
    """
    Fetch all existing seats from the Airplane Ticket doctype.
    """
    seats = frappe.get_all("Airplane Ticket", filters={}, fields=["seat"])
    return {s["seat"] for s in seats if s["seat"]}
