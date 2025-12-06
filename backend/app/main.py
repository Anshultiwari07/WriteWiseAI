from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import GenerateRequest, GenerateResponse
from .agents import run_full_pipeline


app = FastAPI(title="WriteWiseAI Backend")

# ===== CORS for frontend (Vite dev server) =====
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "app": "WriteWiseAI"}


@app.post("/generate", response_model=GenerateResponse)
def generate_content(payload: GenerateRequest):
    result = run_full_pipeline(
        topic=payload.topic,
        format_type=payload.format_type,
        length=payload.length,
        num_pieces=payload.num_pieces,
        language=payload.language,
    )
    return GenerateResponse(**result)
