# /// script
# requires-python = ">=3.12"
# dependencies = [ "pandas==2.2.3", "httpx==0.28.1"]
# ///

"""Collects report.json files from multiple sources and generates a simple report."""

import json
import os
import sys
from pathlib import Path

import httpx
import pandas as pd

first_arg = sys.argv[1]

dir_path = Path(first_arg)

reports = []

for directory in dir_path.iterdir():
    if not directory.is_dir():
        continue

    report_file_path = directory / "report.json"

    with open(report_file_path, "r") as f:
        report = json.load(f)
        report["name"] = directory.name
        reports.append(report)

reports.sort(key=lambda x: "".join(x["name"].split("-")[2:-1]) + x["name"].split("-")[1] + x["name"].split("-")[-1])

df = pd.DataFrame(reports)


def generate_report(df):
    report_str = []

    report_str.append("# Benchmark Report")
    report_str.append(f"**PR Number**: {os.getenv('PR_NUMBER')}")

    report_str.append("\n## Detailed Results")
    report_str.append("| Test Name | Success Count | Elapsed Time (s) | Requests Count |")
    report_str.append("|-----------|---------------|------------------| ---------------|")

    for _, row in df.iterrows():
        report_str.append(
            f"| {row['name']} | {row['success_count']} | {row['elapsed_time']:.4f} | {row['requests_count']} |"
        )

    return "\n".join(report_str)


# Example usage
# Assuming `reports` is already defined
markdown_report = generate_report(df)
print(markdown_report)


def post_github_comment(comment_message: str):
    repo_owner = os.getenv("GITHUB_REPOSITORY_OWNER")
    repo_name = os.getenv("GITHUB_REPOSITORY").split("/")[1]
    pr_number = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")

    if not all([repo_owner, repo_name, pr_number, comment_message, token]):
        raise ValueError("Missing required environment variables.")

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"

    payload = {"body": f"{comment_message}"}

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    with httpx.Client() as client:
        response = client.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        return "Comment posted successfully!"
    else:
        return f"Failed to post comment: {response.status_code}, {response.text}"


post_github_comment(comment_message=generate_report(df))
