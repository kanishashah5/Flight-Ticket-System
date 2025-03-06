import frappe

def before_save(doc, method):
    doc.full_name = f"{doc.first_name} {doc.last_name or ''}".strip()


