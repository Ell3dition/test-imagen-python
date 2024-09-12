# External
from fastapi import FastAPI

# Project
from app.routers import centers, necropsy_analysis, necropsy_cases, necropsy_diagnostic

app = FastAPI()

app.router.prefix = "/necropsy"
app.include_router(centers.router)
app.include_router(necropsy_cases.router)
app.include_router(necropsy_analysis.router)
app.include_router(necropsy_diagnostic.router)


@app.get("/health")
def read_root():
    return {"status": "ok"}
