from fastapi import FastAPI, Depends, Query, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from crud import cities as city_crud
from db.database import SessionLocal
from schemas.cities import CityListSchema, CityRetrieveSchema, CityCreateSchema, CityUpdateSchema

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/cities/", response_model=CityListSchema)
def city_list(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: Session = Depends(get_db),
):
    total_items = city_crud.get_total_cities_count(db)
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No cities found.")

    total_pages = (total_items + per_page - 1) // per_page
    cities = city_crud.get_all_cities(db, skip=(page - 1) * per_page, limit=per_page)

    prev_page = f"/cities/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/cities/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return CityListSchema(
        cities=cities,
        total_items=total_items,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page
    )


@router.get("/cities/{city_id}", response_model=CityRetrieveSchema)
def get_one_author(
        city_id: int,
        db: Session = Depends(get_db)
):
    city = city_crud.get_city_by_id(city_id=city_id, db=db)
    if not city:
        raise HTTPException(status_code=404, detail="City with the given ID was not found.")
    return CityRetrieveSchema.model_validate(city)


@router.post("/cities/", response_model=CityRetrieveSchema)
def create_city(
        city_data: CityCreateSchema,
        db: Session = Depends(get_db)
):
    db_city = city_crud.get_city_by_name(db=db, city_name=city_data.name)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="City with such title is already exist."
        )

    return city_crud.create_city(db=db, city_data=city_data)


@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(city_id: int, db: Session = Depends(get_db)):
    city = city_crud.get_city_by_id(city_id=city_id, db=db)

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City with the given ID was not found."
        )

    db.delete(city)
    db.commit()

    return {"detail": "City deleted successfully."}


@router.patch("/movies/{movie_id}/")
def update_movie(
    city_id: int,
    city_data: CityUpdateSchema,
    db: Session = Depends(get_db),
):
    city = city_crud.get_city_by_id(db, city_id=city_id)

    data_to_update = city_data.model_dump(exclude_unset=True)
    for field, value in data_to_update.items():
        setattr(city, field, value)
    db.commit()
    db.refresh(city)
    return {"detail": "City updated successfully."}
