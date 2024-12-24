from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

# Load OpenAI API key from environment variable
client = OpenAI()

# Initialize FastAPI app
app = FastAPI()

# Define request model
class LessonRequest(BaseModel):
    topic: str
    language: str

# Define response model
class LessonResponse(BaseModel):
    topic: str
    language: str
    lesson_content: str

@app.post("/generate-lesson/", response_model=LessonResponse)
async def generate_lesson(request: LessonRequest):
    """
    Generate a programming lesson for a given topic and language using OpenAI API.
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

    try:
        # Call OpenAI API to generate the lesson
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        # Extract content from OpenAI's response
        lesson_content = response.choices[0].message.content
        
        # Package the response as JSON (assuming the response is formatted correctly)
        return LessonResponse(
            topic=request.topic,
            language=request.language,
            lesson_content=lesson_content
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate lesson: {str(e)}")

# Run the app using uvicorn (e.g., uvicorn lesson_generator_api:app --reload)

# latest error:
# {"detail":"Failed to generate lesson: 'str' object has no attribute 'get'"}