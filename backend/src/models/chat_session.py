"""
ChatSession Model - Technical consultation chat history
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import Base


class ChatSession(Base):
    """
    Technical consultation chat - questions and LLM responses
    Used for exercise technique, equipment alternatives, concepts
    """

    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Chat content
    question = Column(Text, nullable=False)  # User's question (max 1000 chars enforced in Pydantic)
    response = Column(Text, nullable=False)  # LLM response
    question_category = Column(
        String(50), nullable=False
    )  # "technique", "equipment", "concept", "injury_caution"

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="chat_sessions")

    def __repr__(self):
        return f"<ChatSession(id={self.id}, user_id={self.user_id}, category={self.question_category})>"
