import frappe


def set_status_completed(doc, method=None):
    doc.db_set("status", "Completed")

