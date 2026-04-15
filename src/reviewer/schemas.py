from pydantic import BaseModel, Field

class CodeReview(BaseModel):
    pep8_violations: list[str] = Field(description="Список порушень PEP 8 (назва файла на початку)")
    vulnerabilities: list[str] = Field(description="Список вразливостей (назва файла на початку)")
    refactoring_suggestions: str = Field(description="Поради з покращення (назва файла на початку та після назви починається новий рядок)")
    complexity_score: int = Field(
        description="Оцінка якості коду від 1 до 10. 10 - ідеальний код без помилок, 1 - критично поганий код.",
        ge=1, le=10
    )