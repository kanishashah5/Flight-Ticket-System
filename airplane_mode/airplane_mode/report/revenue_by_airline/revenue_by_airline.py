# Copyright (c) 2025, A and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint

def execute(filters=None):
    data, columns = [], []

    columns = get_columns()
    airline_revenue = get_airline_revenue()

    if not airline_revenue:
        msgprint(_('No records found'))
        return columns, airline_revenue

    total_revenue = sum(d.get("revenue", 0) for d in airline_revenue)

    data = []
    for d in airline_revenue:
        row = frappe._dict({
            "airline": d.get("airline"),
            "revenue": d.get("revenue", 0)
        })
        data.append(row)

    data.append({
        "airline": "Total",
        "revenue": total_revenue,
    	"style": "font-weight: bold;"
    })
    


    chart = get_chart_data(data[:-1])  
    report_summary = get_report_summary(total_revenue)

    return columns, data, None, chart, report_summary

def get_columns():
    return [
        {
            "fieldname": "airline",
            "label": _("Airline"),
            "fieldtype": "Link",
            "options": "Airline",
            "width": "200"
        },
        {
            "fieldname": "revenue",
            "label": _("Revenue"),
            "fieldtype": "Currency",
            "width": "150"
        }
    ]

def get_airline_revenue():
    airlines = frappe.get_all("Airline", pluck="name")

    tickets = frappe.get_all(
        "Airplane Ticket",
        fields=["flight", "total_amount"]
    )

    flight_names = list(set(ticket["flight"] for ticket in tickets if ticket["flight"]))
    flights = frappe.get_all(
        "Airplane Flight",
        filters={"name": ["in", flight_names]},
        fields=["name", "airplane"]
    )

    airplane_names = list(set(flight["airplane"] for flight in flights if flight["airplane"]))
    airplanes = frappe.get_all(
        "Airplane",
        filters={"name": ["in", airplane_names]},
        fields=["name", "airline"]
    )

    flight_to_airplane = {flight["name"]: flight["airplane"] for flight in flights}
    airplane_to_airline = {airplane["name"]: airplane["airline"] for airplane in airplanes}

    revenue_dict = {airline: 0 for airline in airlines}

    for ticket in tickets:
        flight = ticket["flight"]
        airplane = flight_to_airplane.get(flight)
        airline = airplane_to_airline.get(airplane)
        if airline:
            revenue_dict[airline] += ticket["total_amount"]

    return [{"airline": airline, "revenue": revenue} for airline, revenue in revenue_dict.items()]

def get_chart_data(data):
    if not data:
        return None

    labels = [entry["airline"] for entry in data]
    values = [entry["revenue"] for entry in data]

    return {
        "data": {
            "labels": labels,
            "datasets": [{"values": values}]
        },
        "type": "donut"
    }

def get_report_summary(total_revenue):
    return [
        {
            "value": total_revenue,
            "indicator": "Green",
            "label": "Total Revenue",
            "datatype": "Currency",
        }
    ]
