from pydantic import BaseModel, Field


class SyllabusText(BaseModel):
    text: str

class GradeTier(BaseModel):
    letter: str = Field(description="Letter grade, e.g., 'A', 'B+', 'Pass'")
    min_pct: float = Field(description="Minimum percentage threshold")
    max_pct: float = Field(description="Maximum percentage threshold")

class SyllabusGradingScale(BaseModel):
    grading_scale: list[GradeTier]