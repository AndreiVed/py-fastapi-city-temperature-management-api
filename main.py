from fastapi import FastAPI

from city.routes import router as city_router


app = FastAPI(
    title="City temperature management",
    description="Homework project"
)

app.include_router(city_router, tags=["city"])
