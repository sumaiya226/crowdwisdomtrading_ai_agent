import os, re
from typing import Tuple
try:
    from litellm import completion as llm_completion
except Exception:
    llm_completion = None

POS_WORDS = {"bullish","great","love","impressive","strong","solid","rocket","moon","up","buy","long"}
NEG_WORDS = {"bearish","sell","selling","trim","cautious","worries","stretched","risks","miss","down","short"}

def _rule_based_sentiment(text: str) -> Tuple[str, float, str]:
    t = text.lower()
    pos = sum(w in t for w in POS_WORDS)
    neg = sum(w in t for w in NEG_WORDS)
    score = (pos - neg) / 3.0
    score = max(min(score, 1.0), -1.0)
    label = "neutral"
    if score > 0.2: label = "positive"
    elif score < -0.2: label = "negative"
    subject = "markets"
    m = re.search(r"\$([A-Za-z]{1,5})", text)
    if m:
        subject = f"${{m.group(1).upper()}}"
    return label, score, subject

class SentimentEngine:
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm and llm_completion is not None and bool(os.getenv("LITELLM_MODEL"))

    def classify(self, text: str) -> Tuple[str, float, str]:
        if not self.use_llm:
            return _rule_based_sentiment(text)

        prompt = f"""
        You are a precise financial sentiment tagger.
        For the tweet: ```{text}```
        1) sentiment: one of positive, negative, neutral
        2) sentiment_score: float in [-1,1]
        3) subject: short phrase (e.g., "$TSLA", "market", "macro")
        Return JSON only: {{"sentiment": "...", "sentiment_score": 0.0, "subject": "..."}}
        """
        try:
            resp = llm_completion(model=os.getenv("LITELLM_MODEL"),
                                  messages=[{"role":"user","content":prompt}])
            content = resp["choices"][0]["message"]["content"]
            import json as _json, re as _re
            s = _re.search(r"\{.*\}", content, _re.S)
            data = _json.loads(s.group(0)) if s else {}
            label = data.get("sentiment","neutral")
            score = float(data.get("sentiment_score", 0.0))
            subject = data.get("subject","markets")
            score = max(min(score, 1.0), -1.0)
            if label not in {"positive","negative","neutral"}:
                label = "neutral"
            return label, score, subject
        except Exception:
            return _rule_based_sentiment(text)