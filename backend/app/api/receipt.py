from fastapi import APIRouter, UploadFile, File
from app.services.ocr_service import extract_text
from app.services.categorize import categorize_item
from app.services.carbon_calc import calculate_co2
from app.services.db_service import save_receipt


router = APIRouter(
    prefix="/receipt",
    tags=["Receipt"]
)


@router.post("/upload")
async def upload_receipt(file: UploadFile = File(...)):
    # 1. OCR
    text = extract_text(file.file)
 
    # 2. Split text into lines (simple parsing)
    lines = text.split("\n")

    items = []
    total_co2 = 0.0

    # 3. Categorize + calculate CO₂
    for line in lines:
        if line.strip() == "":
            continue

        category = categorize_item(line)
        co2 = calculate_co2(category)

        items.append({
            "item": line,
            "category": category,
            "co2": co2
        })

        total_co2 += co2

    save_receipt(items, total_co2)
   

    # 4. Return result
    return {
        "items": items,
        "total_co2": round(total_co2, 2)
    }
