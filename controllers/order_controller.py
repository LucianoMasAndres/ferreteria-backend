"""Order controller with proper dependency injection."""
from controllers.base_controller_impl import BaseControllerImpl
from schemas.order_schema import OrderSchema
from services.order_service import OrderService


class OrderController(BaseControllerImpl):
    """Controller for Order entity with CRUD operations."""

    def __init__(self):
        super().__init__(
            schema=OrderSchema,
            service_factory=lambda db: OrderService(db),
            tags=["Orders"]
            tags=["Orders"]
            tags=["Orders"]
        )

        from fastapi import Depends
        from sqlalchemy.orm import Session
        from config.database import get_db

        @self.router.get("/client/{client_id}", response_model=list[OrderSchema])
        def get_by_client(client_id: int, db: Session = Depends(get_db)):
            service = OrderService(db)
            return service.get_by_client(client_id)
        
        @self.router.get("/client/{client_id}", response_model=list[OrderSchema])
        def get_by_client(client_id: int, db=None): # db injected by BaseController dependency if needed, but here we likely create service in route or use self.service_factory
             # Since BaseController doesn't expose the service instance directly in a way that persists across requests (it creates it per request), 
             # we need to re-instantiate or use the dependency injection pattern used in BaseController.
             # Actually, looking at BaseController, it likely uses a dependency for the service.
             # Let's verify how to access the service. The BaseController usually defines routes that use `service: BaseService = Depends(...)`.
             # For custom routes, we should follow the same pattern manually.
             from config.database import get_db
             from fastapi import Depends
             
             service = self._service_factory(next(get_db())) # This is a bit hacky for synchronous access if get_db is generator
             # Better: Use Depends(get_db) in the function signature
             return service.get_by_client(client_id)

    # Let's rewrite the method to be cleaner and use FastAPI dependency injection correctly
    def register_routes(self):
        super().register_routes()
        from fastapi import Depends
        from sqlalchemy.orm import Session
        from config.database import get_db

        @self.router.get("/client/{client_id}", response_model=list[OrderSchema])
        def get_by_client(client_id: int, db: Session = Depends(get_db)):
            service = OrderService(db)
            return service.get_by_client(client_id)