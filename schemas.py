"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Research website schemas

class Profile(BaseModel):
    """Single profile document for the site"""
    name: str = Field(..., description="Your full name")
    title: Optional[str] = Field(None, description="Professional title")
    bio: Optional[str] = Field(None, description="Short bio shown on homepage")
    avatar_url: Optional[HttpUrl] = Field(None, description="Link to profile image")
    location: Optional[str] = Field(None, description="Location")
    email: Optional[str] = Field(None, description="Public email for contact")
    website: Optional[HttpUrl] = Field(None, description="Personal website or lab site")
    twitter: Optional[str] = Field(None, description="Twitter/X handle or URL")
    github: Optional[str] = Field(None, description="GitHub handle or URL")
    google_scholar: Optional[HttpUrl] = Field(None, description="Google Scholar URL")
    orcid: Optional[str] = Field(None, description="ORCID identifier")

class Publication(BaseModel):
    """Publications collection schema"""
    title: str = Field(..., description="Paper title")
    abstract: Optional[str] = Field(None, description="Abstract or summary")
    authors: List[str] = Field(default_factory=list, description="List of authors in order")
    venue: Optional[str] = Field(None, description="Conference or Journal name")
    year: Optional[int] = Field(None, description="Publication year")
    month: Optional[str] = Field(None, description="Publication month (e.g., May)")
    doi: Optional[str] = Field(None, description="DOI string")
    pdf_url: Optional[HttpUrl] = Field(None, description="Link to the PDF")
    project_url: Optional[HttpUrl] = Field(None, description="Project page or code repository")
    tags: List[str] = Field(default_factory=list, description="Keywords or categories")
    featured: bool = Field(False, description="Feature this on the homepage")
    slug: Optional[str] = Field(None, description="URL-friendly identifier derived from title")
