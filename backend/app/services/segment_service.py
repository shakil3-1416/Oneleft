import json

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.segment import Segment


def get_segment_customers(
    segment_id: int,
    db: Session
):
    segment = (
        db.query(Segment)
        .filter(Segment.id == segment_id)
        .first()
    )

    if not segment:
        return []

    rules = json.loads(segment.rule_json)

    query = db.query(Customer)

    if "category" in rules:
        query = query.filter(
            Customer.category == rules["category"]
        )

    return query.all()