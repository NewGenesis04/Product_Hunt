from pydantic import BaseModel, Field
from typing import Literal, Any
from datetime import datetime

class ComparisonCriterion(BaseModel):
    name: str = Field(..., description="The name of the criterion (e.g., 'Price', 'Battery Life')")
    weight: float = Field(..., ge=0.0, le=1.0, description="The importance weight of this criterion (0.0 to 1.0)")
    intent: Literal["minimize", "maximize", "target"] = Field(..., description="The optimization goal (e.g., minimize price, maximize battery)")
    target_value: Any | None = Field(default=None, description="The specific target value if intent is 'target'")

class NormalizedFeature(BaseModel):
    feature_name: str = Field(..., description="The standardized name of the feature being compared")
    unit: str | None = Field(default=None, description="The unit of measurement (e.g., 'USD', 'hours', 'GB')")
    values: dict[int, Any] = Field(..., description="A mapping of Product ID to its normalized value for this feature")

class Tradeoff(BaseModel):
    description: str = Field(..., description="A natural language description of the tradeoff")
    advantage: str = Field(..., description="What is gained (e.g., '20% cheaper')")
    sacrificed: str = Field(..., description="What is lost (e.g., 'No manufacturer warranty')")
    impact_score: float = Field(..., description="A normalized score (-1.0 to 1.0) representing the net impact of this tradeoff")

class RankedProduct(BaseModel):
    product_id: int = Field(..., description="The ID of the product being ranked")
    rank: int = Field(..., description="The position in the ranking (1 is best)")
    total_score: float = Field(..., description="The calculated score based on weighted criteria")
    match_reasoning: str = Field(..., description="Why this product received this score")
    key_tradeoffs: list[Tradeoff] = Field(default_factory=list, description="The specific tradeoffs identified for this product relative to the ideal")

class ProductComparison(BaseModel):
    id: str = Field(..., description="Unique identifier for this comparison session")
    timestamp: datetime = Field(..., description="When this comparison was generated")
    criteria: list[ComparisonCriterion] = Field(..., description="The criteria used for this comparison")
    product_ids: list[int] = Field(..., description="The list of product IDs included in this comparison")
    feature_grid: list[NormalizedFeature] = Field(..., description="The normalized side-by-side data used for reasoning")
    ranked_results: list[RankedProduct] = Field(..., description="The final ranked list of products")
    summary_verdict: str = Field(..., description="A high-level summary of the comparison outcome for the user")