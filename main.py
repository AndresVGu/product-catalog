from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Product Catalog API running"}
