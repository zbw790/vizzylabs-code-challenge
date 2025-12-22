from fastapi import FastAPI
from database import Base, engine
from routes import creators, analytics
from seed_data import seed_database

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed database with test data
seed_database()

app = FastAPI(
    title="Creator Mobile Backend API",
    description="Backend API for creator discovery and analytics mobile app",
    version="1.0.0"
)

# Include routers
app.include_router(creators.router)
app.include_router(analytics.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Creator Mobile Backend API is running"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected"
    }
