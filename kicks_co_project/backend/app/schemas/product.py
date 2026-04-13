from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    brand: str
    name: str
    category: str
    price: float
    resell_price: float
    badge: str
    image_url: str

    model_config = {'from_attributes': True}
