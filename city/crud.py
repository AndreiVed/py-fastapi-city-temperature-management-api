from sqlalchemy.orm import Session

from city.models import CityModel
from city.schemas import CityCreateSchema


def get_all_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CityModel).offset(skip).limit(limit).all()


def get_total_cities_count(db: Session):
    return db.query(CityModel).count()


def get_city_by_id(db: Session, city_id: int):
    city = db.query(CityModel).filter(CityModel.id==city_id).first()
    return city


def get_city_by_name(db: Session, city_name: str):
    city = db.query(CityModel).filter(CityModel.name==city_name).first()
    return city


def create_city(db: Session, city_data: CityCreateSchema):
    db_author = CityModel(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author