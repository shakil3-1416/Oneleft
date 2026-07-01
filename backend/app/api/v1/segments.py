from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from app.models.customer import Customer
from app.services.segment_service import get_segment_customers
from app.schemas.customer import CustomerResponse
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.segment import Segment
from app.models.store import Store
from app.schemas.segment import SegmentCreate
from app.schemas.segment import SegmentResponse

router = APIRouter(
    prefix="/segments",
    tags=["Segments"]
)


@router.post("/", response_model=SegmentResponse)
def create_segment(
    payload: SegmentCreate,
    db: Session = Depends(get_db)
):
    store = db.query(Store).filter(
        Store.id == payload.store_id
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    segment = Segment(
        store_id=payload.store_id,
        name=payload.name,
        description=payload.description,
        rule_json=payload.rule_json
    )

    db.add(segment)
    db.commit()
    db.refresh(segment)

    return segment


@router.get("/", response_model=list[SegmentResponse])
def list_segments(
    db: Session = Depends(get_db)
):
    return db.query(Segment).all()


@router.get("/{segment_id}", response_model=SegmentResponse)
def get_segment(
    segment_id: int,
    db: Session = Depends(get_db)
):
    segment = db.query(Segment).filter(
        Segment.id == segment_id
    ).first()

    if not segment:
        raise HTTPException(
            status_code=404,
            detail="Segment not found"
        )
@router.get(
    "/{segment_id}/customers",
    response_model=list[CustomerResponse]
)
def segment_customers(
    segment_id: int,
    db: Session = Depends(get_db)
):
    return get_segment_customers(
        segment_id,
        db
    )
    return segment
