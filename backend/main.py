from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.tasks import router as tasks_router
from routes.chat import router as chat_router
import traceback

#app = FastAPI()
app = FastAPI(redirect_slashes=False)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"GLOBAL EXCEPTION: {exc}")
    print(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000" ,"https://your-vercel-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def Root():
    return "I am OK!"

app.include_router(tasks_router)
app.include_router(chat_router)