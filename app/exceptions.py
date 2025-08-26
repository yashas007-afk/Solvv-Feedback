from fastapi import FastAPI
from fastapi.responses import JSONResponse

class FeedbackNotFoundError(Exception):
    def __init__(self, feedback_id: int):
        self.feedback_id = feedback_id
        super().__init__(f"Feedback with ID {feedback_id} not found")

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(FeedbackNotFoundError)
    async def feedback_not_found_handler(_, exc: FeedbackNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})