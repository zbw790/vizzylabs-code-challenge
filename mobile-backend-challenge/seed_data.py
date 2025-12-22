"""
Seed database with test data for the coding challenge
Creates 100 creators and 10 videos per creator (1000 total videos)
"""
from database import SessionLocal, engine
from models import Base, Creator, Video
from datetime import datetime, timedelta
import random


def seed_database():
    """Populate database with test data"""
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if already seeded
        existing_creators = db.query(Creator).count()
        if existing_creators > 0:
            print(f"Database already seeded with {existing_creators} creators")
            return

        print("Seeding database with test data...")

        # Create 100 creators
        creators = []
        for i in range(1, 101):
            creator = Creator(
                username=f"creator_{i}",
                display_name=f"Creator {i}",
                follower_count=random.randint(1000, 1000000),
                total_views=random.randint(10000, 10000000),
                avg_engagement_rate=random.uniform(0.01, 0.15),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365))
            )
            creators.append(creator)

        db.add_all(creators)
        db.commit()

        # Create 10 videos per creator (1000 total)
        videos = []
        for creator in creators:
            for j in range(1, 11):
                view_count = random.randint(100, 1000000)
                like_count = int(view_count * random.uniform(0.01, 0.20))
                comment_count = int(view_count * random.uniform(0.001, 0.05))

                video = Video(
                    creator_id=creator.id,
                    title=f"{creator.display_name}'s Video #{j}",
                    view_count=view_count,
                    like_count=like_count,
                    comment_count=comment_count,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 180))
                )
                videos.append(video)

        db.add_all(videos)
        db.commit()

        print(f"✅ Successfully seeded database with {len(creators)} creators and {len(videos)} videos")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
