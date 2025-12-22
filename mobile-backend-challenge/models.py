from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Creator(Base):
    __tablename__ = "creators"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    display_name = Column(String)
    follower_count = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    avg_engagement_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    videos = relationship("Video", back_populates="creator")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creators.id"))
    title = Column(String)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("Creator", back_populates="videos")


# Index for common queries
Index('idx_video_creator_views', Video.creator_id, Video.view_count)
