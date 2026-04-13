from datetime import datetime
from pydantic import BaseModel


class AuctionResponse(BaseModel):
    id: int
    name: str
    image_url: str
    current_bid: float
    ends_at: datetime

    model_config = {'from_attributes': True}
