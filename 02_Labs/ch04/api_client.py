"""api_client.py - call a web API and handle errors properly.

Example target: the public GitHub API (no key needed for light use).

Usage:
    python3 api_client.py octocat
    python3 api_client.py some-user-that-does-not-exist   # shows 404 handling

Optional: set GITHUB_TOKEN in your environment for a higher rate limit.
    export GITHUB_TOKEN="your_token_here"   # never hard-code tokens in the file
"""

import os
import sys
import time

import requests

BASE_URL = "https://api.github.com"
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def get_json(url, params=None, timeout=5, retries=3):
    """GET a URL and return parsed JSON, or None if it fails.

    Retries on timeouts, connection errors and temporary server errors,
    waiting 1s, 2s, 4s... between attempts.
    """
    headers = {"Accept": "application/json", "User-Agent": "cybershield-lab"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for attempt in range(1, retries + 1):
        wait = 2 ** (attempt - 1)
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)

            if response.status_code in RETRYABLE_STATUS and attempt < retries:
                print(f"Server returned {response.status_code}. Retrying in {wait}s...")
                time.sleep(wait)
                continue

            response.raise_for_status()  # raises for any remaining 4xx/5xx
            return response.json()       # raises ValueError if not valid JSON

        except requests.exceptions.Timeout:
            print(f"Timed out (attempt {attempt}/{retries}).")
        except requests.exceptions.ConnectionError:
            print(f"Could not connect (attempt {attempt}/{retries}).")
        except requests.exceptions.HTTPError as exc:
            code = exc.response.status_code
            if code == 401:
                print("Unauthorized: check your API token.")
            elif code == 403:
                print("Forbidden or rate limited: wait a while or use a token.")
            elif code == 404:
                print("Not found: check the URL or username.")
            elif code == 429:
                print("Rate limited: too many requests. Try again later.")
            else:
                print(f"HTTP error {code}: {exc.response.text[:200]}")
            return None  # client errors will not fix themselves, so do not retry
        except ValueError:
            print("The response was not valid JSON.")
            return None
        except requests.exceptions.RequestException as exc:
            print(f"Request failed: {exc}")
            return None

        if attempt < retries:
            time.sleep(wait)

    print("Giving up after repeated failures.")
    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 api_client.py USERNAME")
        sys.exit(1)

    username = sys.argv[1]
    data = get_json(f"{BASE_URL}/users/{username}")
    if data is None:
        sys.exit(1)

    print(f"User:         {data.get('login')}")
    print(f"Name:         {data.get('name') or 'n/a'}")
    print(f"Public repos: {data.get('public_repos')}")
    print(f"Followers:    {data.get('followers')}")
    print(f"Profile:      {data.get('html_url')}")


if __name__ == "__main__":
    main()
