# ai-edtech-api
An api for generating lessons for any programming language.

# Getting started
specify your OPENAI_API_KEY=<your-proj-api-key-here> in .env

install dependencies
```bash
pip install pydantic fastapi dotenv uvicorn
```
run the api server locally
```bash
uvicorn lesson_generator_api:app --reload
```

open another terminal

```bash
curl -X POST "http://localhost:8000/generate-lesson/" -H "Content-Type: application/json" -d '{"topic": "For Loops", "language": "Python"}'
```

Change topic and language values to whatever you want.