from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Mentor(SQLModel, table=True):
    __tablename__ = "mentors"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    company: Optional[str] = None
    title: Optional[str] = None
    avatar_url: Optional[str] = None
    tech_stack: str = Field(description="Comma separated list of technologies")

    def get_tech_stack(self) -> List[str]:
        return [s.strip() for s in self.tech_stack.split(",")] if self.tech_stack else []
