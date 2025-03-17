import frappe


def set_status_completed(doc, method=None):
    doc.db_set("status", "Completed")

def update_flight_tickets_gate(doc, method):
	updated_gate_number = doc.gate_no

	tickets = frappe.get_all("Airplane Ticket", filters={"flight": doc.name}, fields=["name"])

	for ticket in tickets:
		ticket_doc = frappe.get_doc("Airplane Ticket", ticket["name"])
		
		ticket_doc.gate_no = updated_gate_number
		ticket_doc.save()

	frappe.msgprint(f"All tickets for flight {doc.name} have been updated with the new gate number.")