from pydantic import BaseModel, Field

class PokemonBase(BaseModel):
    name: str
    type_: str = Field(..., alias="type")
    region: str
    sprite_url: str

    class Config:
        orm_mode = True
        # this allows FastAPI to use SQLAlchemy models directly
        populate_by_name = True
