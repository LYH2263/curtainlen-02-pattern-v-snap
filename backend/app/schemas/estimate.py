from typing import Optional
from pydantic import BaseModel, Field

class EstimateRequest(BaseModel):
    window_id: int
    fabric_id: int
    # 当次试算花高（厘米）；不传则用布料默认花高。负数直接 422，不会落 calc_runs
    pattern_height_cm: Optional[float] = Field(default=None, ge=0)
    save: bool = False
    note: str = ""

class FabricPatternHeightRequest(BaseModel):
    pattern_height_cm: float = Field(ge=0)
