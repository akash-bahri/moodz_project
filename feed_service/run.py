import uvicorn
from fastapi import FastAPI
from app.routes import router

app = FastAPI()

# Include the feed-related routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=5003, reload=True)
