import frappe

def before_save(doc, method=None):
    first_name = doc.first_name 
    last_name = doc.last_name
    doc.full_name = f"{first_name} {last_name}".strip()