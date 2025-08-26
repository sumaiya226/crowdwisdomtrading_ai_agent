from typing import List, Dict, Any
from .tools.x_scraper_tool import XScraperTool
from .processing.sentiment import SentimentEngine
from .guardrails.validation import UserResultSchema
from .processing.tickers import extract_tickers_and_directions
import os, json

class XDataCollectorAgent:
    """Collect X data for a user via scraping tools or mock samples."""
    def __init__(self, use_llm: bool):
        self.tool = XScraperTool()

    def run(self, username: str) -> Dict[str, Any]:
        data = self.tool.fetch_user_tweets(username=username, max_count=200)
        return data

class SentimentAgent:
    """Analyze per-tweet sentiment and subject via LLM or offline fallback."""
    def __init__(self, use_llm: bool):
        self.engine = SentimentEngine(use_llm=use_llm)

    def run(self, username: str, tweets: List[str]) -> Dict[str, Any]:
        per_tweet = []
        for t in tweets:
            label, score, subject = self.engine.classify(text=t)
            per_tweet.append({"text": t, "sentiment": label, "score": score, "subject": subject})

        sentiments = [p["score"] for p in per_tweet]
        avg = sum(sentiments)/len(sentiments) if sentiments else 0.0
        tickers = extract_tickers_and_directions([p["text"] for p in per_tweet])

        return {"username": username, "per_tweet": per_tweet, "avg_sentiment": avg, "tickers": tickers}

class StructurerAgent:
    """Validate & normalize output JSON with guardrails (pydantic)."""
    def run(self, username: str, analyzed: Dict[str, Any]) -> Dict[str, Any]:
        validated = UserResultSchema.model_validate(analyzed)
        return validated.model_dump()

class ReporterAgent:
    """Generate a PDF report with per-user summaries and optional YouTube RAG snippets."""
    def __init__(self, outdir: str, youtube_ids: List[str] = None):
        self.outdir = outdir
        self.youtube_ids = youtube_ids or []

    def run(self, summary):
        from .reports.pdf_report import build_pdf_report
        build_pdf_report(summary.model_dump() if hasattr(summary, "model_dump") else summary,
                         outpath=os.path.join(self.outdir, "report.pdf"),
                         youtube_ids=self.youtube_ids)