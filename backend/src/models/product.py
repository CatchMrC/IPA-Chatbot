from pydantic import BaseModel
from typing import Optional, Dict, Any

class ProductQuery(BaseModel):
    query: str
    include_advice: Optional[bool] = False
    filters: Optional[Dict[str, Any]] = None
    single_product: Optional[bool] = True