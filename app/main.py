import uvicorn
from fastapi import FastAPI

from api import ROUTERS


app = FastAPI(title="Wallet API", version="0.0.1")

for router in ROUTERS:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
