from fastapi import FastAPI

app = FastAPI(title="Stock AI")

@app.get("/")
def root():
    return {
        "message": "Stock AI Backend Running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
