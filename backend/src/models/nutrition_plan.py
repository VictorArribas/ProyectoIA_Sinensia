"""
NutritionPlan Model - Calculated macros and TDEE
"""
from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import Base


class NutritionPlan(Base):
    """
    Calculated nutrition plan - TDEE and macros
    Auto-recalculated when user updates weight
    """

    __tablename__ = "nutrition_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Calculated values
    tdee = Column(Float, nullable=False)  # Total Daily Energy Expenditure (kcal)
    protein_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fat_g = Column(Float, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="nutrition_plans")

    def __repr__(self):
        return f"<NutritionPlan(id={self.id}, user_id={self.user_id}, tdee={self.tdee})>"
