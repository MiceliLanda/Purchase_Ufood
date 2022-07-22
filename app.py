from fastapi import FastAPI
import uvicorn
from routes.user import userRoute

app = FastAPI()
app.include_router(userRoute)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9000, reload=True)