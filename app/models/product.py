from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class Specifications(BaseModel):
    source: Literal["manufacturer", "consensus", "mixed"] = Field(..., description="The source of the specifications")
    data: dict = Field(..., description="The specifications data as a dictionary")

class PriceStats(BaseModel):
    average_price: float = Field(..., description="The average price of the product")
    median_price: float = Field(..., description="The median price of the product")
    min_price: float = Field(..., description="The minimum price of the product")
    max_price: float = Field(..., description="The maximum price of the product")

class ProductSnapshot(BaseModel):
    name: str = Field(..., description="The name of the product")
    brand: str = Field(..., description="The brand associated with the product")
    specifications: Specifications = Field(..., description="The specifications of the product")

class MarketSummary(BaseModel):
    price_stats: PriceStats = Field(..., description="The price statistics of the product")
    vendors_count: int = Field(..., description="The number of vendors offering the product")
    confidence_score: float = Field(..., description="The confidence score of the market data")

class VendorOfferings(BaseModel):
    id: int = Field(..., description="The unique identifier for the product")
    vendor_name: str = Field(..., description="The name of the vendor")
    price: float = Field(..., description="The price offered by the vendor")
    listing_url: str = Field(..., description="The URL of the vendor's listing for the product")
    availability: Literal["in_stock", "out_of_stock", "pre_order"] = Field(..., description="The availability status of the product from the vendor")
    warranty: str | None = Field(default=None,description="The warranty information provided by the vendor")
    timestamp: datetime = Field(..., description="The timestamp when the offering was recorded")

class Product(BaseModel):
    id: int = Field(..., description="The unique identifier for the product queried")
    snapshot: list[ProductSnapshot]
    market_summary: MarketSummary
    vendor_offerings: list[VendorOfferings] | None
    timestamp: datetime