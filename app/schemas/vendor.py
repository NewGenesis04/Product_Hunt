from pydantic import BaseModel, Field
from typing import Literal, Set
from datetime import datetime

class VendorTrustSignal(BaseModel):
    source: str = Field(..., description="Where this signal came from (e.g., 'User Feedback', 'Platform Rating')")
    score: float = Field(..., ge=0.0, le=1.0, description="Normalized trust score (0.0 to 1.0)")
    evidence: str = Field(..., description="Short text evidence (e.g., 'Delivered 2 days late')")
    timestamp: datetime = Field(default_factory=datetime.now)

class VendorProfile(BaseModel):
    name: str = Field(..., description="The vendor's distinct name (e.g., 'GadgetDepot')")
    platform: str = Field(..., description="The platform they operate on (e.g., 'Jumia', 'Konga', 'Instagram', 'Direct')")
    domain_url: str | None = Field(None, description="Main URL for the vendor")
    operating_locations: Set[str] = Field(default_factory=set, description="Known locations they ship from/to (e.g., 'Lagos', 'Abuja')")
    delivery_reliability: Literal["unknown", "fast", "average", "slow", "unreliable"] = "unknown"
    
    # Trust & Reputation (Derived from Memory)
    trust_score: float = Field(0.5, ge=0.0, le=1.0, description="Aggregate trust score. Starts neutral (0.5).")
    observations: list[VendorTrustSignal] = Field(default_factory=list, description="List of specific trust signals recorded")

    last_seen: datetime = Field(default_factory=datetime.now)
