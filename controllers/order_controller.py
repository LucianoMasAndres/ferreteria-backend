"""Order controller with proper dependency injection."""
from controllers.base_controller_impl import BaseControllerImpl
from schemas.order_schema import OrderSchema
from services.order_service import OrderService
from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db

class OrderController(BaseControllerImpl):
    """Controller for Order entity with CRUD operations."""

    def __init__(self):
        super().__init__(
            schema=OrderSchema,
            service_factory=lambda db: OrderService(db),
            tags=["Orders"]
        )
        
        # Register custom endpoints
        @self.router.get("/client/{client_id}", response_model=list[OrderSchema])
        def get_by_client(client_id: int, db: Session = Depends(get_db)):
            service = OrderService(db)
            return service.get_by_client(client_id)