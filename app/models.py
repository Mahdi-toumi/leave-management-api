from pydantic import BaseModel

class LeaveRequest(BaseModel):
    employee_id: int
    reason: str
    days: int
    status: str = "Pending"