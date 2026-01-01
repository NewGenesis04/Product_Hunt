from pydantic import BaseModel, Field
from typing import Literal, Any
from datetime import datetime
import uuid

class EpisodeStatus(BaseModel):
    state: Literal["active", "paused", "completed", "abandoned"] = "active"
    last_transition_reason: str | None = None

class Episode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: EpisodeStatus = Field(default_factory=EpisodeStatus)
    
    # Contextual Anchors
    category: str = Field(..., description="The product category (e.g., 'Monitors')")
    initial_query: str = Field(..., description="The user's first query that started this episode")
    extracted_constraints: dict[str, Any] = Field(default_factory=dict, description="Parsed constraints like budget, brand, specs")
    
    # References
    product_ids: list[int] = Field(default_factory=list, description="IDs of products explored in this episode")
    comparison_id: str | None = Field(None, description="Link to the ProductComparison schema if one was generated")
    
    # Temporal Data
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_interaction_at: datetime = Field(default_factory=datetime.now)

class Preference(BaseModel):
    category: str = Field(..., description="The category this preference applies to (or 'global')")
    feature: str = Field(..., description="The specific attribute (e.g., 'brand', 'warranty_length', 'vendor_reliability')")
    value: Any = Field(..., description="The preferred value or range")
    preference_type: Literal["like", "dislike", "must_have", "dealbreaker"] = "like"
    
    # Weight & Confidence
    confidence: float = Field(0.5, ge=0.0, le=1.0, description="How sure we are about this preference")
    evidence_count: int = Field(1, description="Number of times this preference has been reinforced")
    
    last_updated: datetime = Field(default_factory=datetime.now)

class Heuristic(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Short name for the heuristic (e.g., 'Nigerian Warranty Premium')")
    rule: str = Field(..., description="Natural language description of the rule")
    applicability: dict[str, Any] = Field(..., description="When to apply this (e.g., {'category': 'electronics'})")
    logic_hint: str = Field(..., description="Instruction for the agent on how to use this (e.g., 'Add 10% weight to price if vendor is official store')")
