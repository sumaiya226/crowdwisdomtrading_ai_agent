from typing import List, Dict
from pydantic import BaseModel, Field

class TweetAnalysis(BaseModel):
    text: str
    sentiment: str = Field(pattern="^(positive|negative|neutral)$")
    score: float = Field(ge=-1.0, le=1.0)
    subject: str

class TickerDirection(BaseModel):
    ticker: str = Field(pattern="^[A-Z]{1,5}$")
    direction: str = Field(pattern="^(bullish|bearish|neutral|unknown)$")
    confidence: float = Field(ge=0.0, le=1.0)

class UserResultSchema(BaseModel):
    username: str
    per_tweet: List[TweetAnalysis]
    avg_sentiment: float = Field(ge=-1.0, le=1.0)
    tickers: List[TickerDirection] = []

class SummarySchema(BaseModel):
    users_processed: List[str]
    results: Dict[str, UserResultSchema]
    errors: Dict[str, str]