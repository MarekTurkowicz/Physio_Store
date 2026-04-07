"""Reports endpoint — manually trigger sales report generation (manager only)."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, field_validator

from app.dependencies import require_manager
from app.models.user import User
from app.schemas.common import MessageResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

VALID_PERIODS = {"daily", "weekly", "monthly"}


class ReportRequest(BaseModel):
    period: str = "weekly"

    @field_validator("period")
    @classmethod
    def validate_period(cls, v: str) -> str:
        if v not in VALID_PERIODS:
            raise ValueError(f"period must be one of: {', '.join(sorted(VALID_PERIODS))}")
        return v


@router.post("/generate", response_model=MessageResponse)
async def generate_report(
    data: ReportRequest,
    current_manager: User = Depends(require_manager),
) -> MessageResponse:
    """
    Trigger an async sales report for the given period.

    The report is built and emailed to the requesting manager in the
    background by a Celery worker — this endpoint returns immediately.

    - **daily**   → last 24 hours
    - **weekly**  → last 7 days
    - **monthly** → last 30 days
    """
    from app.tasks.report_tasks import generate_sales_report

    generate_sales_report.delay(
        period=data.period,
        manager_email=current_manager.email,
    )

    period_label = {"daily": "dzienny", "weekly": "tygodniowy", "monthly": "miesięczny"}
    return MessageResponse(
        message=f"Raport {period_label[data.period]} jest generowany.",
        detail=f"Wynik zostanie przesłany na: {current_manager.email}",
    )
