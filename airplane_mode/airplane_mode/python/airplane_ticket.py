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

def get_existing_seats():
    seats = frappe.get_all("Airplane Ticket", filters={}, fields=["seat"])
    return {s["seat"] for s in seats if s["seat"]}


def validate(doc, method=None):
    unique_addons = {}

    filtered_addons = []
    for addon in doc.get not in unique_addons:
            unique_addons[addon.item] = addon
            filtered_addons.append(addon)

   
    doc.set("add_ons", filtered_addons)

def prevent_submission(doc, method):
    if doc.status != "Boarded":
        frappe.throw("You cannot submit this ticket because the passenger has not boarded yet!")

