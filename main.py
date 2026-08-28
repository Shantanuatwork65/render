from fastapi import FastAPI, Request
from bs4 import BeautifulSoup
import requests
import time
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from config import settings
app = FastAPI()

limiter=Limiter(key_func=get_remote_address)
app.state.limiter=limiter

#Error handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request:Request, exc:RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Rate limit exceeded. Please try again later."},
    )   



url="https://indianexpress.com/"

cache_storage = []
last_cache_time = 0
cache_expiration = settings.CACHE_EXPIRATION
rate_limit=settings.RATE_LIMIT

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/news")
@limiter.limit(f"{rate_limit}/minute")
def read_news(request:Request,page:int=1, limit:int=5):
    global cache_storage, last_cache_time, cache_expiration
    headlines = []
    start_time = time.time()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    if time.time() - last_cache_time < cache_expiration and cache_storage:
        print("Using cached data...")
        headlines = cache_storage
    else:
        print("Fetching new data from the website...")
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = []
        for item in soup.find_all("a", class_="topblockNews__sidebarLink"):
            headlines.append(item.text.strip())
        cache_storage = headlines
        last_cache_time = time.time()

    end_time = time.time()
    print(f"Time taken to fetch and parse the data: {end_time - start_time} seconds")

    start_index = (page - 1) * limit
    end_index = start_index + limit
    headlines = headlines[start_index:end_index]

    return {
        "page": page,
        "limit": limit,
        "headlines": headlines,
        "time_taken": end_time - start_time
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)