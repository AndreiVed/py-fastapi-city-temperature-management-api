from fastapi import FastAPI

from routes.cities import router as city_router


app = FastAPI(
    title="City temperature management homework",
    description="Description of project"
)


app.include_router(city_router, tags=["city"])
