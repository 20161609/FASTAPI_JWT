from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, TIMESTAMP

from app.db.init import Base


class Auth(Base):
    __tablename__ = "auth"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    create_time = Column(TIMESTAMP, default=datetime.utcnow)
    update_time = Column(TIMESTAMP, default=datetime.utcnow)


class Token(Base):
    __tablename__ = "token"

    token_id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("auth.uid"), nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    expires_at = Column(TIMESTAMP, nullable=False)
