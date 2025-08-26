import os, json, argparse
from dotenv import load_dotenv
from src.flow import OrchestratorFlow

def parse_args():
    p = argparse.ArgumentParser(description="CrowdWisdomTrading AI Agent - CLI")
    p.add_argument("--usernames-file", required=True, help="File with one X username per line")
    p.add_argument("--outdir", required=True, help="Output directory")
    p.add_argument("--use-llm", action="store_true", help="Enable LLM via litellm (requires keys)")
    p.add_argument("--youtube-ids", nargs="*", default=[], help="Optional YouTube IDs to include in report")
    return p.parse_args()

def main():
    load_dotenv(override=True)
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    with open(args.usernames_file, "r", encoding="utf-8") as f:
        usernames = [ln.strip() for ln in f if ln.strip()]

    flow = OrchestratorFlow(use_llm=args.use_llm, outdir=args.outdir, youtube_ids=args.youtube_ids)
    summary = flow.run(usernames=usernames)
    sum_path = os.path.join(args.outdir, "summary.json")
    with open(sum_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote consolidated summary: {sum_path}")
    print(f"PDF report: {os.path.join(args.outdir, 'report.pdf')}")

if __name__ == "__main__":
    main()