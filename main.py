#!/usr/bin/env python3
import requests
import os
import sys
from dotenv import load_dotenv
import argparse
load_dotenv()

headers = {"Authorization": os.getenv("TOKEN")}


def is_inactive_user(user):
    # not a github user
    if user is None:
        return False

    # take older accounts
    if int(user["createdAt"][0:4]) > 2011:
        return False

    curr_user = []

    curr_user.append(user["starredRepositories"]["totalCount"])
    curr_user.append(user["repositories"]["totalCount"])
    curr_user.append(
        user["contributionsCollection"]["totalCommitContributions"]
    )
    curr_user.append(
        user["contributionsCollection"]["restrictedContributionsCount"]
    )
    curr_user.append(user["following"]["totalCount"])
    curr_user.append(
        0
        if user["contributionsCollection"]["hasAnyContributions"] is False
        else 1
    )

    return sum(curr_user) < 1

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--inp', help='input file')
    parser.add_argument('-o', '--out', help='output file')

    args = parser.parse_args()

    if not args.inp or not args.out:
        print("Must provide valid I/O files.", file=sys.stderr)
        sys.exit(1)

    with open(args.inp, "r") as users:
        with open(args.out, "w") as output:

            for user in users:
                res = build_query(user.rstrip())["data"]
                if is_inactive_user(res["user"]):
                    print("OK!\nUser: {}".format(user))
                    output.write("{}\n".format(user))


def run_query(query, variables):
    request = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers,
    )
    if request.status_code == 200:
        return request.json()
    else:
        raise requests.HTTPError(
            "Query failed to run by returning code of {}. {}".format(
                request.status_code, query
            )
        )


def build_query(user):
    query = """
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
        }"""

    variables = {"login": user}
    return run_query(query, variables)


if __name__ == "__main__":
    main()
