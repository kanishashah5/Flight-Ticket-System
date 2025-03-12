import frappe
import random


def before_save(doc, method=None):
  
    total_addon_amount = sum([addon.amount for addon in doc.get("add_ons", []) if addon.amount])
    doc.total_amount = doc.flight_price + total_addon_amount


    if not doc.seat:
        existing_seats = get_existing_seats()
        
        while True:
            row = random.randint(1, 50)  # Rows from 1 to 50
            seat_letter = random.choice(["A", "B", "C", "D", "E"])  # Seat letters
            seat = f"{row}{seat_letter}"

            if seat not in existing_seats:
                doc.seat = seat
                break

def get_existing_seats(flight):
    seats = frappe.get_all("Airplane Ticket", filters={"flight": flight}, fields=["seat"])
    return {s["seat"] for s in seats if s["seat"]}



def validate(doc, method=None):

    unique_addons = {}
    filtered_addons = []
    for addon in doc.get("add_ons", []):
        if addon.item not in unique_addons:
            unique_addons[addon.item] = addon
            filtered_addons.append(addon)

        # Get the airplane linked to the flight
    airplane = frappe.db.get_value("Airplane Flight", doc.flight, "airplane")

    if not airplane:
        frappe.throw("The selected flight does not have a linked airplane.")

    # Get the airplane's seat capacity
    capacity = frappe.db.get_value("Airplane", airplane, "capacity")

    if not capacity:
        frappe.throw(f"The airplane {airplane} does not have a defined capacity.")

    # Count existing tickets for this flight, including the one being saved
    booked_tickets = frappe.db.count("Airplane Ticket", {"flight": doc.flight}) + 1  # Add 1 for current doc

    # Ensure capacity is not exceeded
    if booked_tickets > capacity:
        frappe.throw(f"No available seats! The airplane capacity ({capacity}) has been reached.")

    # Assign a unique seat if not already assigned
    if not doc.seat:
        existing_seats = get_existing_seats(doc.flight)

        while True:
            row = booked_tickets  # Sequentially assign seat row
            seat_letter = ["A", "B", "C", "D", "E", "F"][booked_tickets % 6]  # Rotate seat letters
            seat = f"{row}{seat_letter}"

            if seat not in existing_seats:
                doc.seat = seat
                break


def prevent_submission(doc, method):
    if doc.status != "Boarded":
        frappe.throw("You cannot submit this ticket because the passenger has not boarded yet!")

