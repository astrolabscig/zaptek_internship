from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import applications

app = FastAPI(title="Zaptek Internship Applications API")

app.include_router(applications.router)


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {"status": exc.status_code, "message": exc.detail},
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    details = []
    for err in exc.errors():
        field = ".".join(str(part) for part in err["loc"][1:])
        message = err["msg"].replace("Value error, ", "")
        details.append({"field": field, "message": message})

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {"status": 422, "message": "Invalid data", "details": details},
        },
    )


@app.get("/")
def root():
    return {"message": "Zaptek Applications API is running", "docs": "/docs"}