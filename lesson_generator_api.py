from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
import asyncio
import os

load_dotenv()

# Load OpenAI API key from environment variable
client = OpenAI()

# Initialize FastAPI app
app = FastAPI()

# Define request model
class LessonRequest(BaseModel):
    topic: str
    language: str

@app.get("/generate-lesson-stream/")
async def generate_lesson_stream(request: LessonRequest):
    """
    Stream a programming lesson for a given topic and language using OpenAI API.
    """
    prompt = f"""
    Topic: {request.topic}
    Language: {request.language}

    Create a structured lesson with:
    1. A concise explanation of the topic.
    2. An example code snippet in {request.language} with comments.
    3. Three challenges:
       - Beginner: A simple task to introduce the topic.
       - Intermediate: A task combining this concept with another basic one.
       - Advanced: A problem-solving task applying the concept in a real-world context.
    Include detailed instructions, hints, and solutions for each challenge.
    """

    async def lesson_generator():
        try:
            # Call OpenAI API with streaming enabled
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                stream=True  # Enable streaming
            )
            
            # Stream the response chunks
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield f"data: {content}\n\n"  # Send SSE formatted data
                await asyncio.sleep(0)  # Yield control to the event loop
            yield "data: [DONE]\n\n"  # Indicate the end of the stream
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(lesson_generator(), media_type="text/event-stream")