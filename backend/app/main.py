from fastapi import FastAPI

from app.api.v1.customers import router as customer_router
from app.api.v1.stores import router as store_router
from app.api.v1.products import router as product_router
from app.api.v1.segments import router as segment_router
from app.api.v1.campaigns import router as campaign_router


app = FastAPI(
    title="OneLeft API",
    version="0.1.0",
    description="AI Marketing Automation Platform"
)


# -----------------------------
# API Routers
# -----------------------------

app.include_router(
    store_router,
    prefix="/api/v1"
)

app.include_router(
    customer_router,
    prefix="/api/v1"
)

app.include_router(
    product_router,
    prefix="/api/v1"
)

app.include_router(
    segment_router,
    prefix="/api/v1"
)

app.include_router(
    campaign_router,
    prefix="/api/v1"
)


# -----------------------------
# Root
# -----------------------------

@app.get("/")
def root():
    return {
        "app": "OneLeft",
        "message": "API is running"
    }


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }