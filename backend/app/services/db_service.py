from app.config.firebase import db
from datetime import datetime, timezone, timedelta

def save_receipt(items, total_co2):
    now = datetime.now(timezone.utc)

    data = {
        "items": items,
        "total_co2": total_co2,
        "created_at": now,                       # ✅ timezone-aware
        "date": now.strftime("%Y-%m-%d")         # for UI grouping
    }

    db.collection("receipts").add(data)


def get_all_receipts():
    receipts = []
    docs = db.collection("receipts").stream()

    for doc in docs:
        receipts.append(doc.to_dict())

    return receipts
