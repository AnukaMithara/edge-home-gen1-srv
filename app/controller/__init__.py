from fastapi import APIRouter
from starlette.responses import HTMLResponse

from app.controller.user_controller import router as user_router
from app.controller.device_controller import router as device_router
from app.controller.device_logs_controller import router as device_logs_router
from app.controller.user_logs_controller import router as user_logs_router

all_routers = APIRouter()
all_routers.include_router(user_router)
all_routers.include_router(device_router)
all_routers.include_router(device_logs_router)
all_routers.include_router(user_logs_router)


@all_routers.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
        <head>
            <title>Edge Home API Service</title>
        </head>
        <body>
            <h1>Welcome to Edge Home API Service</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
