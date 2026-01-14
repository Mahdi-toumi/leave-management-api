import structlog
from fastapi import APIRouter, HTTPException
from app.models import LeaveRequest

logger = structlog.get_logger()
router = APIRouter()
db: dict[int, LeaveRequest] = {}

@router.post("/leaves/", status_code=201)
async def create_leave(leave: LeaveRequest):
    logger.info("create_leave_attempt", employee_id=leave.employee_id)
    
    if leave.employee_id in db:
        logger.error("leave_creation_failed", reason="duplicate_id", employee_id=leave.employee_id)
        raise HTTPException(status_code=400, detail="Leave request already exists")
    
    db[leave.employee_id] = leave
    logger.info("leave_created_success", employee_id=leave.employee_id, days=leave.days)
    return {"message": "Request created", "data": leave}

@router.get("/leaves/{employee_id}")
async def get_leave(employee_id: int):
    if employee_id not in db:
        logger.warning("leave_not_found", employee_id=employee_id)
        raise HTTPException(status_code=404, detail="Not found")
    
    logger.info("leave_retrieved", employee_id=employee_id)
    return db[employee_id]