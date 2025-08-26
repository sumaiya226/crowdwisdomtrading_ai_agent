import re
from typing import List, Dict

BULL_HINTS = ["bull", "bullish", "buy", "long", "load", "add", "accumulate", "moon", "rocket", "upside"]
BEAR_HINTS = ["bear", "bearish", "sell", "short", "trim", "cut", "downside", "risk", "dump"]

def extract_tickers_and_directions(texts: List[str]) -> List[Dict]:
    counts = {}
    for t in texts:
        for m in re.findall(r"\$([A-Za-z]{1,5})", t):
            tk = m.upper()
            d = counts.setdefault(tk, {"bull":0,"bear":0,"neu":0})
            tl = t.lower()
            if any(h in tl for h in BULL_HINTS):
                d["bull"] += 1
            elif any(h in tl for h in BEAR_HINTS):
                d["bear"] += 1
            else:
                d["neu"] += 1
    out = []
    for tk, d in counts.items():
        total = max(d["bull"]+d["bear"]+d["neu"], 1)
        if d["bull"] > d["bear"]:
            dirn = "bullish"; conf = d["bull"]/total
        elif d["bear"] > d["bull"]:
            dirn = "bearish"; conf = d["bear"]/total
        else:
            dirn = "neutral"; conf = d["neu"]/total
        out.append({"ticker": tk, "direction": dirn, "confidence": round(conf, 3)})
    return out