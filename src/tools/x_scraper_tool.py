import os, json

class XScraperTool:
    """Stub for MCP/BrightData or other scraping providers. Uses samples in mock mode."""
    def __init__(self):
        self.samples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "samples", "tweets"))

    def fetch_user_tweets(self, username: str, max_count: int = 200):
        sample_path = os.path.join(self.samples_dir, f"{username}.json")
        if os.path.exists(sample_path):
            with open(sample_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            tweets = data.get("tweets", [])[:max_count]
            return {"username": username, "tweets": tweets}
        return {"username": username, "tweets": []}