from fastapi import APIRouter
from datetime import datetime, timedelta
from app.services.db_service import get_all_receipts

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/")
def get_analytics():
    """
    Returns:
    - total emissions
    - daily breakdown
    - weekly breakdown (last 7 days)
    - monthly breakdown
    """

    receipts = get_all_receipts()

    total_emissions = 0.0
    daily_data = {}
    weekly_data = {}
    monthly_data = {}

    today = datetime.now().date()
    last_7_days = today - timedelta(days=7)

    for receipt in receipts:
        try:
            date_obj = datetime.strptime(receipt["date"], "%Y-%m-%d").date()
            co2 = receipt["total_co2"]
        except Exception:
            continue  # skip malformed data

        total_emissions += co2

        # ---- DAILY ----
        day_key = date_obj.strftime("%Y-%m-%d")
        daily_data[day_key] = daily_data.get(day_key, 0) + co2

        # ---- WEEKLY (last 7 days only) ----
        if date_obj >= last_7_days:
            week_key = date_obj.strftime("%Y-%m-%d")
            weekly_data[week_key] = weekly_data.get(week_key, 0) + co2

        # ---- MONTHLY ----
        month_key = date_obj.strftime("%Y-%m")
        monthly_data[month_key] = monthly_data.get(month_key, 0) + co2

    return {
        "total_emissions": round(total_emissions, 2),
        "daily_breakdown": daily_data,
        "weekly_breakdown": weekly_data,
        "monthly_breakdown": monthly_data
    }
