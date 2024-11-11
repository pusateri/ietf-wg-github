"""
This script gets the issues from an IETF working group
"""

from urllib.request import Request, urlopen
from datetime import datetime
import time
import argparse
import json

BASE_URL = "https://api.github.com/repos/"


def request_issues(owner, repo, issues_filename, sort, direction):

    if issues_filename:
        with open(issues_filename, 'r', encoding='UTF-8') as file:
            contents = str(file.read())
    else:
        req = Request(
            BASE_URL + "{}/{}/issues?sort={}&direction={}&per_page=40".format(
                owner, repo, sort, direction
            ),
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "87f7811a9fde3055c99abc7e977172978745badf",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urlopen(req) as response:
            contents = response.read()

    return json.loads(contents)


def request_labels(owner, repo, labels_filename, number):
    if labels_filename:
        with open(labels_filename, 'r', encoding='UTF-8') as file:
            contents = str(file.read())
    else:
        req = Request(
            BASE_URL + "{}/{}/issues/{}/labels".format(owner, repo, number),
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "87f7811a9fde3055c99abc7e977172978745badf",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urlopen(req) as response:
            contents = response.read()

    return json.loads(contents)


def request_comments(owner, repo, comments_filename):
    if comments_filename:
        with open(comments_filename, 'r', encoding='UTF-8') as file:
            contents = str(file.read())
    else:
        req = Request(
            BASE_URL + "{}/{}/issues/comments".format(owner, repo),

            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "87f7811a9fde3055c99abc7e977172978745badf",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urlopen(req) as response:
            contents = response.read()

    return json.loads(contents)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", type=str, default="ietf-wg-emailcore")
    parser.add_argument("--repo", type=str, default="emailcore")
    parser.add_argument("--comments-filename", type=str)
    parser.add_argument("--issues-filename", type=str)
    parser.add_argument("--labels-filename", type=str)
    parser.add_argument("--sort-created", type=str)
    parser.add_argument("--sort-updated", type=str)
    parser.add_argument("--sort-ascending", type=str)
    parser.add_argument("--sort-descending", type=str)
    args = parser.parse_args()

    sort = "updated"
    if args.sort_updated:
        sort = "updated"
    elif args.sort_created:
        sort = "created"

    direction = "desc"
    if args.sort_ascending:
        direction = "asc"
    elif args.sort_descending:
        direction = "desc"

    issues = request_issues(args.owner, args.repo, args.issues_filename, sort, direction)
    # comments = request_comments(args.owner, args.repo, args.comments_filename, sort, direction)
    for issue in issues:
        user = issue.get("user")
        if user:
            login = user.get("login")
            updated_str = issue.get("updated_at")
            created_str = issue.get("created_at")
            if updated_str and created_str:
                number = issue.get("number")
                time.sleep(1)  # don't overrun github API
                label_objs = request_labels(args.owner, args.repo, args.labels_filename, number)
                labels = list(map(lambda label: label.get("name"), label_objs))
                try:
                    updated = datetime.fromisoformat(updated_str)
                    created = datetime.fromisoformat(created_str)
                    print(issue.get("title"))
                    print(
                        "#{}".format(number),
                        created.strftime('created %Y-%m-%d'),
                        "by {}".format(login),
                        updated.strftime('(updated %Y-%m-%d)'),
                    )
                    if labels:
                        print("labels: {}".format(", ".join(labels)))
                    print("")
                except ValueError:
                    pass


if __name__ == "__main__":
    main()
