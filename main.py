from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from ddgs import DDGS
import ollama
import os

app = FastAPI()

# CORS (For development - adjust for production)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuration ---
MODEL_NAME = "gemma3:4b"
PERSONALITY_PROMPTS = {
    "The Scholar": "You are a brilliant, highly educated expert in your field. Respond with detailed explanations and technical terminology. Limit your response to 200 characters.",
    "The Optimist": "You are an eternally cheerful and enthusiastic guide. Focus on the positive aspects and motivational benefits. Limit your response to 200 characters.",
    "The Skeptic": "You are a cynical observer questioning conventional wisdom. Respond with caution and critical analysis. Question assumptions. Limit your response to 200 characters.",
    "The Minimalist": "You are a simple, practical person focused on easy, achievable solutions. Keep your response concise and straightforward. Limit your response to 200 characters.",
    "The Creative": "You are a creative and passionate innovator, focusing on the interesting and imaginative approaches to any topic. Limit your response to 200 characters.",
    "The Mentor": "You are a compassionate and understanding advisor explaining the importance of a particular concept for growth and development. Limit your response to 200 characters.",
    "The Performer": "You are a dedicated professional who needs this concept for peak performance. Focus on the impact to performance. Limit your response to 200 characters.",
    "The Traditionalist": "You are someone sharing insights from historic practices and perspectives. Limit your response to 200 characters.",
    "The Environmentalist": "You are someone sharing insights on how to approach this topic with environmental responsibility. Limit your response to 200 characters.",
}

# --- Helper Functions ---


def get_personality_response(personality_name: str, question: str) -> str:
    """Retrieves a response from a specific personality."""
    if personality_name not in PERSONALITY_PROMPTS:
        raise HTTPException(status_code=404, detail="Personality not found")

    prompt = f"{PERSONALITY_PROMPTS[personality_name]}\n\nQuestion: {question}\nAnswer:"
    try:
        return ollama.generate(model="tinyllama", prompt=prompt).response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response from {personality_name}: {e}",
        )


def synthesize_responses(personality_responses: Dict[str, str], question: str) -> str:
    """Combines personality responses using an LLM."""
    prompt = f"""You are a helpful summarization bot. You are provided with multiple answers to a question, each from a different perspective.

    {personality_responses}

    Synthesize a final, comprehensive answer that incorporates the best aspects of all responses,
    while preserving the unique perspectives of each personality. Clearly attribute insights to each original perspective
    as appropriate. Maintain a professional and engaging tone.
    """

    try:
        return ollama.generate(model="gemma3:12b", prompt=prompt).response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error synthesizing responses: {e}"
        )


# --- API Endpoints ---
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Context must be a dictionary and *must* include the request object
    context = {"request": request, "name": "User"}
    return templates.TemplateResponse(name="index.html", context=context)


@app.get("/all_personalities")
async def get_all_personalities(
    question: str = Query(..., description="The question to ask the personalities")
):
    """Retrieves responses from all personalities and combines them."""
    personality_responses = {}
    try:
        for personality_name in PERSONALITY_PROMPTS:
            personality_responses[personality_name] = get_personality_response(
                personality_name, question
            )

        combined_response = synthesize_responses(personality_responses, question)

        return {
            "personalities": personality_responses,
            "combined_response": combined_response,
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@app.get("/personality/{personality_name}")
async def get_personality_response_endpoint(
    personality_name: str,
    question: str = Query(..., description="The question to ask."),
):
    """Retrieves a response from a specific personality."""
    try:
        response = get_personality_response(personality_name, question)
        return {"personality": personality_name, "response": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while retrieving response: {e}",
        )


# --- Run the Application ---

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
