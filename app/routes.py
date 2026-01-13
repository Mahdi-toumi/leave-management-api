from fastapi import APIRouter, HTTPException
from app.models import LeaveRequest

router = APIRouter()
db: dict[int, LeaveRequest] = {}  # In-memory database

@router.post("/leaves/", status_code=201)
async def create_leave(leave: LeaveRequest):
    if leave.employee_id in db:
        raise HTTPException(status_code=400, detail="Leave request already exists")
    db[leave.employee_id] = leave
    return {"message": "Request created", "data": leave}

@router.get("/leaves/{employee_id}")
async def get_leave(employee_id: int):
    if employee_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    return db[employee_id]