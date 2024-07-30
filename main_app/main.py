from fastapi import FastAPI, Request
from ai_engine.ai_engine import AIEngine

app = FastAPI()

# Initialize AIEngine with global options
ai_engine = AIEngine(
    base_url="https://api.openai.com/v1",
    default_model="gpt-4o"
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    print("Request Data:", data)  # Add this line to print the request data
    user_id = data["user_id"]
    user_input = data["input"]
    response = await ai_engine.process_request(user_id, user_input)
    return response

@app.get("/demonstrate_tooldefs")
async def demonstrate_tooldefs():
    response = await ai_engine.demonstrate_tooldefs()
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
