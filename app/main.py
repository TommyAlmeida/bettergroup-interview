
import uvicorn

from fastapi import FastAPI, Request, Response
from fastapi.openapi.utils import get_openapi

from app.core.config import get_settings

from app.core.middleware import APIKeyMiddleware
from app.features.companies import router as companies
from app.features.analytics import router as analytics
from app.features.projects import router as projects

settings = get_settings()

app = FastAPI(
    title="BetterGroup - Challenge",
    version="1.0.0",
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "APIKey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }

    # We want all routes to have the X-API-KEY available
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"APIKey": []}]

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi
app.add_middleware(APIKeyMiddleware)

app.include_router(companies.router, prefix="/api/v1", tags=["companies"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])
app.include_router(projects.router, prefix="/api/v1", tags=["projects"])


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
        log_level="info")
