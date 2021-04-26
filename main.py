"""collects inactive github usernames"""

import argparse
import os
import sys
from dataclasses import dataclass
import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Candidate:
    """a candidate user"""

    created_at: str
    stars: int
    repos: int
    commits: int
    private_contributions: int
    public_contributions: int
    following: int

    def is_old_account(self) -> bool:
        """checks if the candidates account was created before 2011"""
        return int(self.created_at) < 2011

    def is_inactive(self) -> bool:
        """determines if the candidate is inactive based on stats"""
        return (
            sum(
                [
                    self.stars,
                    self.repos,
                    self.commits,
                    self.private_contributions,
                    self.public_contributions,
                    self.following,
                ]
            )
            == 0
        )


class Client:
    """request client"""

    def __init__(self, query: str, headers: dict):
        self.query = query
        self.headers = headers

    def fetch(self, variables: dict):
        """requests the github api with query, headers and variables"""

        res = requests.post(
            "https://api.github.com/graphql",
            json={"query": self.query, "variables": variables},
            headers=self.headers,
        )

        if res.status_code == 200:
            return (res.json(), True)

        return (f"Query failed with code {res.status_code}", False)


def cli():
    """parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file")
    parser.add_argument("-o", "--output", help="output file")
    return parser.parse_args()


def main():
    """entry point"""
    args = cli()

    if not args.input or not args.output:
        print("Must provide valid I/O files.", file=sys.stderr)
        sys.exit(1)

    users = open(args.input, "r")
    output = open(args.output, "w+")

    client = Client(
        """
        query userInfo($login: String!) {
                user(login: $login) {
                  name
                  login
                  createdAt
                  starredRepositories {
                    totalCount
                  }
                  repositories {
                    totalCount
                  }
                  following {
                    totalCount
                  }
                  contributionsCollection {
                    totalCommitContributions
                    restrictedContributionsCount
                    hasAnyContributions
                  }
                }
            }""",
        {"Authorization": os.getenv("TOKEN")},
    )

    for user in users:
        res, status = client.fetch({"login": user.rstrip()})

        if not status:
            print(res)
            continue

        if not res["data"]["user"]:
            continue

        res = res["data"]["user"]

        candidate = Candidate(
            res["createdAt"][0:4],
            res["starredRepositories"]["totalCount"],
            res["repositories"]["totalCount"],
            res["contributionsCollection"]["totalCommitContributions"],
            res["contributionsCollection"]["restrictedContributionsCount"],
            res["following"]["totalCount"],
            res["contributionsCollection"]["hasAnyContributions"],
        )

        if not candidate.is_old_account() or not candidate.is_inactive():
            continue

        print("OK!\nUser: {}".format(user))
        output.write("{}\n".format(user))


if __name__ == "__main__":
    main()
