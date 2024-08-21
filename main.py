import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controller import all_routers
from app.exceptions.exception_handler import add_exception_handler

app = FastAPI(
    description='Edge Home API Service',
    version="1.0",
    title='Edge Home API Service'
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"]
)

app.include_router(all_routers)
add_exception_handler(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
