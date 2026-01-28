"""Order repository for database operations."""
from sqlalchemy.orm import Session

from models.order import OrderModel
from repositories.base_repository_impl import BaseRepositoryImpl
from schemas.order_schema import OrderSchema


class OrderRepository(BaseRepositoryImpl):
    """Repository for Order entity database operations."""

    def __init__(self, db: Session):
        super().__init__(OrderModel, OrderSchema, db)

    def find_by_client(self, client_id: int) -> list[OrderSchema]:
        """Find all orders for a specific client."""
        from sqlalchemy import select
        stmt = select(self.model).where(self.model.client_id == client_id).order_by(self.model.id_key.desc())
        models = self.session.scalars(stmt).all()
        return [self.schema.model_validate(model) for model in models]