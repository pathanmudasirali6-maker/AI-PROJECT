import os
from openai import AsyncOpenAI
import instructor
from schemas.decision import DecisionOutcome

# Initialize Instructor's patched OpenAI client
# Falls back to an empty string to avoid crashes during scaffolding
client = instructor.from_openai(AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "mock-key")))

async def generate_decision(query: str, context: str) -> DecisionOutcome:
    system_prompt = (
        "You are an AI Decision Engine. "
        "Your task is to analyze the user's query and provide a structured comparison "
        "based strictly on the provided context. If the context is insufficient, reflect that in your confidence score."
    )
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini", # or standard gpt-4o
        response_model=DecisionOutcome,
        max_retries=3, # Instructor handles retry on ValidationError
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {context}\n\nDecision Query: {query}"}
        ]
    )
    
    return response
