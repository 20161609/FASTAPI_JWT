from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def test_root():
    return {"message": "The routing is working well."}
