from fastapi import FastAPI
from app.routers import fetchOutlet, chatbot
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow requests from your frontend
origins = [
    "http://localhost:5173",  # Frontend URL
    "http://127.0.0.1:5173",  # Another version for localhost access
    "https://aminnurrasyid.github.io",  # GitHub Pages frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins listed here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(fetchOutlet.router)
app.include_router(chatbot.router)

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}