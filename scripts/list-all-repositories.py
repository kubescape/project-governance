#!/usr/bin/env python3

import sys
import os
from github import Github
from github.GithubException import GithubException
from typing import List

def get_github_token() -> str:
    """Get GitHub token from environment variable"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    return token

def get_org_repos(org: str, token: str) -> List[str]:
    """Get all repositories for a GitHub organization"""
    g = Github(token)
    try:
        organization = g.get_organization(org)
        return [repo.name for repo in organization.get_repos()]
    except GithubException as e:
        print(f"Error: {e.data.get('message', str(e))}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python list-all-repositories.py <organization>")
        sys.exit(1)

    org = sys.argv[1]
    token = get_github_token()

    try:
        repos = get_org_repos(org, token)
        import json
        print(json.dumps(sorted(repos), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

