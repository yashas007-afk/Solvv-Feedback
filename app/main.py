from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from . import models
from .database import engine
from .exceptions import register_exception_handlers
from .routers import health as health_router, feedback as feedback_router


app = FastAPI(title="Feedback Service")

register_exception_handlers(app)

app.include_router(health_router.router)
app.include_router(feedback_router.router)

@app.on_event("startup")
def on_startup() -> None:
    try:
        models.Base.metadata.create_all(bind=engine)
    except OperationalError:
        # Database might not be available at startup; skip auto-creation.
        pass
