"""Client controller with proper dependency injection."""
from controllers.base_controller_impl import BaseControllerImpl
from schemas.client_schema import ClientSchema
from services.client_service import ClientService
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from config.database import get_db
from models.client import ClientModel
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class ClientController(BaseControllerImpl):
    """Controller for Client entity with CRUD operations."""

    def __init__(self):
        """
        Initialize ClientController with dependency injection.

        The service is created per request with the database session.
        """
        super().__init__(
            schema=ClientSchema,
            service_factory=lambda db: ClientService(db),
            tags=["Clients"]
        )
        
        # Register custom endpoints
        @self.router.post("/login", response_model=ClientSchema)
        def login(request: LoginRequest, db: Session = Depends(get_db)):
            """Authenticate a client."""
            client = db.query(ClientModel).filter(ClientModel.email == request.email).first()
            if not client:
                 raise HTTPException(status_code=401, detail="Invalid credentials")
            
            # In a real app, verify hash. Here we use plaintext for demo.
            if client.password != request.password:
                raise HTTPException(status_code=401, detail="Invalid credentials")
                
            return client
