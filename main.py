"""collects inactive github usernames"""

import argparse
import csv
import enum
import json
import os
import sys
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv
from requests import post
from colorama import init, Fore, Style
from progress.bar import IncrementalBar
from progress.spinner import PixelSpinner

load_dotenv()
init()

class Format(enum.Enum):
  """file types as enums"""

  MARKDOWN = 1
  JSON = 2
  CSV = 3
  TEXT = 4

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
    return (sum([
        self.stars,
        self.repos,
        self.commits,
        self.private_contributions,
        self.public_contributions,
        self.following,
    ]) == 0)

class Client:
  """request client"""
  def __init__(self, query: str, headers: dict):
    self.query = query
    self.headers = headers

  def fetch(self, variables: dict):
    """requests the github api with query, headers and variables"""

    res = post(
        "https://api.github.com/graphql",
        json={
            "query": self.query,
            "variables": variables
        },
        headers=self.headers,
    )

    if res.status_code == 200:
      return (res.json(), True)

    return (f"Query failed with code {res.status_code}", False)

class Exporter:
  """handles writing to various file formats"""
  @staticmethod
  def export_results(results: List[dict], path: str, fmt: str):
    """calls write with open output file"""
    with open(path, "w+") as out:
      Exporter.write(Format(Utils.format_to_int(fmt)), results, out)
    print(Fore.WHITE + Style.BRIGHT, f"✨ Successfully exported results to {path} ✨")

  @staticmethod
  def write(fmt: Format, results: List[dict], out: str):
    """builds and writes different outputs based on file format"""
    if fmt == Format.MARKDOWN:
      table = "| User(s) | Created In |\n|---|---|\n"
      for item in results:
        table += f"| [{item['user']}](https://github.com/{item['user']}) | {item['created_at']} |\n"
      out.write(table)

    if fmt == Format.JSON:
      json.dump(results, out, indent=4)

    if fmt == Format.TEXT:
      users = ""
      for item in results:
        users += item["user"] + "\n"
      out.write(users)

    if fmt == Format.CSV:
      writer = csv.DictWriter(out, fieldnames=["User(s)", "Created In"])

      writer.writeheader()

      for item in results:
        writer.writerow({"User(s)": item["user"], "Created In": item["created_at"]})

class Bar(IncrementalBar):
  """custom progress bar"""

  message = "Status"
  suffix = "%(percent).1f%% - ETA %(eta)ds"

class Animate:
  """handles progress bars and spinners"""
  def __init__(self, num):
    self.bar = Bar(max=num)
    self.spinner = PixelSpinner()

  def next(self):
    """advance the spinner and bar to the next iteration in cycle"""
    self.bar.next()
    self.spinner.next()

  def done(self):
    """complete the bar"""
    self.bar.finish()

class Utils:
  """utility functions"""
  @staticmethod
  def verify_file(path):
    """verifies type of output file"""
    _, ext = os.path.splitext(path)
    if ext not in [".md", ".json", ".csv", ".txt"]:
      return (None, False)
    return (ext, True)

  @staticmethod
  def format_to_int(fmt: str):
    """file format string to int"""
    table = {".md": 1, ".json": 2, ".csv": 3, ".txt": 4}
    return table[fmt]

def cli():
  """parse command line arguments"""
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", help="input file")
  parser.add_argument("-o", "--output", help="output file")
  return parser.parse_args()

def main():
  """entry point"""
  args, results = cli(), []

  if not args.input or not args.output:
    print("Must provide valid I/O files.", file=sys.stderr)
    sys.exit(1)

  ext, status = Utils.verify_file(args.output)
  if not status:
    print("Output file must be of type Markdown, CSV, JSON or Text.")
    return

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

  with open(args.input, "r") as users:
    users = users.readlines()

    animate = Animate(len(users))

    for user in users:
      animate.next()

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

      results.append({"user": user.strip(), "created_at": candidate.created_at})

    animate.done()
    Exporter.export_results(results, args.output, ext)

if __name__ == "__main__":
  main()
