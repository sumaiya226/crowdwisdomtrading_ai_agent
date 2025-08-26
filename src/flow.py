import os, json, traceback
from typing import List, Dict, Any
from .agents import XDataCollectorAgent, SentimentAgent, StructurerAgent, ReporterAgent
from .guardrails.validation import SummarySchema

class OrchestratorFlow:
    """Lightweight orchestrator sequencing agents with guardrails (no server/ports)."""
    def __init__(self, use_llm: bool, outdir: str, youtube_ids: list):
        self.use_llm = use_llm
        self.outdir = outdir
        self.youtube_ids = youtube_ids or []
        self.paths = {"json": os.path.join(outdir, "json")}
        os.makedirs(self.paths["json"], exist_ok=True)

        self.collector = XDataCollectorAgent(use_llm=self.use_llm)
        self.sentiment = SentimentAgent(use_llm=self.use_llm)
        self.structurer = StructurerAgent()
        self.reporter = ReporterAgent(outdir=self.outdir, youtube_ids=self.youtube_ids)

    def run(self, usernames: List[str]) -> Dict[str, Any]:
        all_results: Dict[str, Any] = {}
        errors: Dict[str, str] = {}

        for u in usernames:
            try:
                raw = self.collector.run(username=u)
                analyzed = self.sentiment.run(username=u, tweets=raw["tweets"])
                structured = self.structurer.run(username=u, analyzed=analyzed)
                upath = os.path.join(self.paths["json"], f"{u}.json")
                with open(upath, "w", encoding="utf-8") as f:
                    json.dump(structured, f, indent=2)
                all_results[u] = structured
            except Exception as e:
                errors[u] = str(e)
                traceback.print_exc()

        summary = {"users_processed": list(all_results.keys()), "results": all_results, "errors": errors}
        validated = SummarySchema.model_validate(summary)
        self.reporter.run(validated)
        return validated.model_dump()