import frappe
from frappe.utils.data import add_months

def set_default_rent_amount(doc, method):
    if not doc.rent_amount:  
        shop_settings = frappe.get_doc("Airport Shop Settings", "Airport Shop Settings")
        if shop_settings:
            doc.rent_amount = shop_settings.default_rent_amount


def validate_contract_duration(doc, method):
    contract_start_date = doc.contract_start_date
    contract_end_date = doc.contract_end_date
    min_valid_date = add_months(contract_start_date, 1)

    if contract_end_date and min_valid_date:
        if contract_end_date < min_valid_date:
            frappe.throw("The contract should be atleast 1 month!")