import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.routes:app", host="0.0.0.0", port=5003, reload=True)