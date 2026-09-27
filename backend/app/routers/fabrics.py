from fastapi import APIRouter, HTTPException
from app.repositories import fabrics as repo
from app.schemas.estimate import FabricPatternHeightRequest
router = APIRouter()
@router.get("/fabrics")
def list_fabrics(): return {"items": repo.list_fabrics()}
@router.get("/fabrics/{fid}")
def get_fabric(fid: int):
    r = repo.get_fabric(fid)
    if not r: raise HTTPException(404)
    return r
@router.patch("/fabrics/{fid}")
def patch_fabric(fid: int, body: FabricPatternHeightRequest):
    r = repo.set_pattern_height(fid, body.pattern_height_cm)
    if not r: raise HTTPException(404)
    return r
