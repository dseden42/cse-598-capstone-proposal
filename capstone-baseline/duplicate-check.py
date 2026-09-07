# 1. Grab everything coming directly from the preceding Merge node using Native Python syntax
all_incoming_items = _items

invoice = None
existing_bills = []

# 2. Sort the appended stream items out into their respective variables
for item in all_incoming_items:
    # Under native Python mode, n8n passes items as dictionaries containing a "json" key
    payload = item.get("json", {}) if isinstance(item, dict) else {}
    
    # If the item has the 'output' dictionary from LangChain, it's our invoice
    if "output" in payload:
        invoice = payload.get("output")
    # If it has a QBO Bill marker, append it to the bills checklist array
    elif "TotalAmt" in payload:
        existing_bills.append(payload)

# Fallback: if the invoice wasn't nested under 'output', find the object containing total_amount
if not invoice:
    for item in all_incoming_items:
        payload = item.get("json", {}) if isinstance(item, dict) else {}
        if "total_amount" in payload:
            invoice = payload
            break

# 3. Clean and convert the invoice amount safely
raw_invoice_amount = invoice.get("total_amount") if invoice else None
if isinstance(raw_invoice_amount, (int, float)):
    invoice_amount = float(raw_invoice_amount)
else:
    try:
        clean_str = "".join([c for c in str(raw_invoice_amount or "") if c.isdigit() or c in ".-"])
        invoice_amount = float(clean_str)
    except ValueError:
        invoice_amount = None

invoice_date = invoice.get("invoice_date") if invoice else None

# 4. Compare the new invoice against EVERY bill in the appended list
duplicate_bills = []

for bill in existing_bills:
    raw_bill_amount = bill.get("TotalAmt")
    if isinstance(raw_bill_amount, (int, float)):
        bill_amount = float(raw_bill_amount)
    else:
        try:
            clean_bill_str = "".join([c for c in str(raw_bill_amount or "") if c.isdigit() or c in ".-"])
            bill_amount = float(clean_bill_str)
        except ValueError:
            bill_amount = None

    # Check criteria: same total amount (within a penny) AND same invoice date
    is_same_amount = (bill_amount is not None and invoice_amount is not None and abs(bill_amount - invoice_amount) < 0.01)
    is_same_date = (invoice_date and bill.get("TxnDate") == invoice_date)

    if is_same_amount and is_same_date:
        duplicate_bills.append(bill)

# 5. Set the final status indicator string
status = "duplicate" if len(duplicate_bills) > 0 else "ok"

# 6. Return the data back to n8n matching its mandatory {"json": {...}} output dictionary format
return [{
    "json": {
        "status": status,
        "vendor_name": invoice.get("vendor_name") if invoice else "Unknown",
        "invoice_number": invoice.get("invoice_number") if invoice else "Unknown",
        "total_amount": invoice_amount if invoice_amount is not None else 0.0,
        "invoice_date": invoice_date,
        "existing_bill_count_checked": len(existing_bills),
        "duplicate_count_found": len(duplicate_bills),
        "duplicate_bill_ids": [d.get("Id") for d in duplicate_bills if "Id" in d]
    }
}]
