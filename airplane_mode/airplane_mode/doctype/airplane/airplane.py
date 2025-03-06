# Copyright (c) 2025, A and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document


class Airplane(Document):
    def autoname(self):
     
        airline = self.airline.replace(" ", "")
        total_airplane = frappe.db.count("Airplane", {"airline": self.airline}) + 1

 
        airline_number = str(total_airplane).zfill(3)

        self.name = f"{airline}-{airline_number}"
