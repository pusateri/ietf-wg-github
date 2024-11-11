#!/bin/sh
#  for comments use:
#  https://api.github.com/repos/ietf-wg-emailcore/emailcore/issues/comments
curl -I -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/ietf-wg-emailcore/emailcore/issues
