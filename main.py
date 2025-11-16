import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Profile, Publication

app = FastAPI(title="Research Site API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Research Site Backend Running"}

# Health + DB test
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# ----- API Models for requests -----
class ProfileCreate(Profile):
    pass

class PublicationCreate(Publication):
    pass

# ----- Routes -----
@app.get("/api/profile", response_model=Optional[Profile])
def get_profile():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("profile", {}, limit=1)
    if not docs:
        return None
    doc = docs[0]
    # Remove Mongo _id for Pydantic
    doc.pop("_id", None)
    return Profile(**doc)

@app.post("/api/profile")
def create_or_update_profile(payload: ProfileCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    # Upsert: if a profile exists, replace it by inserting new and deleting old
    existing = get_documents("profile", {}, limit=1)
    if existing:
        # Replace by updating existing doc
        doc = payload.model_dump()
        doc.update({"updated_at": __import__("datetime").datetime.utcnow()})
        db["profile"].update_one({"_id": existing[0]["_id"]}, {"$set": doc})
        return {"status": "updated"}
    else:
        _id = create_document("profile", payload)
        return {"status": "created", "id": _id}

@app.get("/api/publications", response_model=List[Publication])
def list_publications(tag: Optional[str] = None, year: Optional[int] = None, featured: Optional[bool] = None):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    query = {}
    if tag:
        query["tags"] = tag
    if year is not None:
        query["year"] = year
    if featured is not None:
        query["featured"] = featured
    docs = get_documents("publication", query)
    out = []
    for d in docs:
        d.pop("_id", None)
        out.append(Publication(**d))
    return out

@app.post("/api/publications")
def add_publication(payload: PublicationCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    _id = create_document("publication", payload)
    return {"status": "created", "id": _id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
