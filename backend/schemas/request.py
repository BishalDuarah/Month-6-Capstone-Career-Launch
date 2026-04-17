from pydantic import BaseModel

class PropertyRequest(BaseModel):
    location: str
    total_sqft: float
    bath: int
    bhk: int