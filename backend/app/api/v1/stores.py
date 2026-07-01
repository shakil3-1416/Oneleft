from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.store import Store
from app.schemas.store import StoreCreate
from app.schemas.store import StoreResponse

router = APIRouter(
    prefix="/stores",
    tags=["Stores"]
)


@router.post("/", response_model=StoreResponse)
def create_store(
    payload: StoreCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Store).filter(
        Store.owner_email == payload.owner_email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Store already exists"
        )

    store = Store(
        name=payload.name,
        owner_email=payload.owner_email,
        subscription_plan=payload.subscription_plan
    )

    db.add(store)
    db.commit()
    db.refresh(store)

    return store


@router.get("/", response_model=list[StoreResponse])
def list_stores(
    db: Session = Depends(get_db)
):
    return db.query(Store).all()


@router.get("/{store_id}", response_model=StoreResponse)
def get_store(
    store_id: int,
    db: Session = Depends(get_db)
):
    store = db.query(Store).filter(
        Store.id == store_id
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    return store
