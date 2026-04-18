from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.views.invitation import router as InvitationRouter
from app.api.views.users import router as UsersRouter
from app.core.security.auth_middleware import auth_middleware

app = FastAPI()
app.middleware("http")(auth_middleware)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title="Invitation API",
        version="1.0.0",
        description="API with JWT Bearer authentication",
        routes=app.routes,
    )

    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    schema["security"] = [{"BearerAuth": []}]  # apply globally
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Home!"}

app.include_router(UsersRouter)
app.include_router(InvitationRouter)