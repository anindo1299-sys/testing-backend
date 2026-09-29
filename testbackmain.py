import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis

from api import user, product, category, review
from core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0
    )
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    yield
    await redis_client.close()



app = FastAPI(
    title="FastAPI E-Com",
    version="1.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:5173",],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


async def validation_exception_handler(request: Request, exc:RequestValidationError):
    friendly_error = []
    for error_details in exc.errors():
        where_it_is = "->".join(str(part) for part in error_details["loc"])
        what_went_wrong = error_details["msg"]
        friendly_error.append({"field": where_it_is, "message": what_went_wrong})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"validation_issues": friendly_error}
    )
app.add_exception_handler(RequestValidationError, validation_exception_handler)

    
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(category.router, prefix="/api/v1/category", tags=["Category"])
app.include_router(product.router, prefix="/api/v1/product", tags=["Product"])
app.include_router(review.router, prefix="/api/v1/review", tags=["Reviews"])

if __name__ == "__main__":
    uvicorn.run("testbackmain:app", host="127.0.0.1", reload=True, port=8000)