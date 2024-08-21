from fastapi import APIRouter
from starlette.responses import HTMLResponse

from app.controller.source_controller import router as source_router

all_routers = APIRouter()
all_routers.include_router(source_router)


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
