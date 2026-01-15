from fastapi import FastAPI
from app.api.receipt import router as receipt_router
from app.api import analytics 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Carbon Receipt Tracker",
    description="Scan receipts and calculate carbon footprint",
    version="1.0"
)

# Register routes
app.include_router(receipt_router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Carbon Receipt Tracker API is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
