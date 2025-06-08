from fastapi import FastAPI
from src.database.database import Base, engine
from src.routes.endpoints import initialize_endpoints
import uvicorn

app = FastAPI(
    title="Sistema Interno OldLuxRentalCar",
    description="API para gestão interna",
    version="1.0.0"
)

initialize_endpoints(app)

def _criar_tabelas():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    _criar_tabelas()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )