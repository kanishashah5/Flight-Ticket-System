import frappe
from frappe.utils import getdate, add_months, today


def before_save(doc, method):

    check_payment_date(doc, method)

    doc.name = f"{doc.shop}-{doc.from_date}-{doc.to_date}"

def before_submit(doc, method):
    check_status_before_submit(doc)

def check_shop_status(doc,method):
    shop_status = frappe.db.get_value("Shop", doc.shop, "status")
    if shop_status != "On Lease":
        frappe.throw("""The "Airport Shop" is not On Lease!""")

def check_payment_date(doc,method):

    if doc.status == "Pending":
        doc.paid_amount = 0  

    shop = doc.shop
    contract_start_date = frappe.db.get_value("Shop", shop, "contract_start_date")
    contract_end_date = frappe.db.get_value("Shop", shop, "contract_end_date")

    shop_rent_list = frappe.db.get_all(
        "Airport Shop Rent",
        filters={"shop": shop},
        fields=["name", "from_date", "to_date"],
        order_by="to_date desc",
    )

    if shop_rent_list:
        last_shop_rent_doc = shop_rent_list[0]

        if last_shop_rent_doc.to_date == contract_end_date:
            frappe.throw("""Extend the contract in "Airport Shop" to create a new "Airport Shop Rent"!""")

        doc.from_date = last_shop_rent_doc.to_date
        doc.to_date = min(add_months(last_shop_rent_doc.to_date, 1), contract_end_date)
    else:
        doc.from_date = contract_start_date
        doc.to_date = add_months(contract_start_date, 1)

def check_status_before_submit(doc):
    if doc.status != "Paid":
        frappe.throw("""You cannot submit without "Paid" Status!""")

def send_rent_reminder():
    rent_reminder = frappe.db.get_single_value("Airport Shop Settings", "enable_rent_reminders")

    if rent_reminder != 1:
        return

    pending_rent_list = []
    current_date = today()

    shop_list = frappe.db.get_all(
        "Shop",
        filters={"status": "On Lease"},
        fields=["name", "shop_name", "airport", "tenant_name", "email", "contract_start_date", "contract_end_date", "rent_amount"],
    )

    for shop in shop_list:
        last_payed_doc_list = frappe.db.get_list(
            "Airport Shop Rent",
            filters={"shop": shop.name, "status": "Paid"},
            fields=["name", "to_date"],
            order_by="to_date desc",
        )

        if last_payed_doc_list:
            last_payed_doc = last_payed_doc_list[0]
            if getdate(last_payed_doc.to_date) < getdate(current_date):
                pending_rent_list.append({
                    "tenant_name": shop.tenant_name,
                    "tenant_email": shop.email,
                    "to_date": last_payed_doc.to_date,
                    "rent_amount": shop.rent_amount,
                    "shop": shop.name,
                    "shop_name": shop.shop_name,
                    "airport": shop.airport,
                })
        else:
            pending_rent_list.append({
                "tenant_name": shop.tenant_name,
                "tenant_email": shop.email,
                "to_date": shop.contract_start_date,
                "rent_amount": shop.rent_amount,
                "shop": shop.name,
                "shop_name": shop.shop_name,
                "airport": shop.airport,
            })

    for data in pending_rent_list:
        recipient = data["tenant_email"] or ""
        subject = "Rent Reminder!"
        message = f"""
        <div class="message">
            <p>Hello <b>{data["tenant_name"]}</b>,<br>
            Your Rent Amount <b>{data["rent_amount"]}</b> has been pending from <b>{data["to_date"]}</b> for your shop
            <b>{data["shop_name"]}</b> in Airport <b>{data["airport"]}</b>. Please pay your rent.<br>
            Thank You.</p>
        </div>
        """

        frappe.sendmail(
            recipients=recipient,
            subject=subject,
            message=message,
        )
