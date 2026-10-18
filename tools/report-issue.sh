#!/bin/bash
# Keeps one open issue per check: a non-empty report opens it (or updates the open one), an empty one closes it.
#   tools/report-issue.sh "TITLE" REPORT_FILE "INTRO"
# Needs gh and GH_TOKEN (the workflow's token, with issues: write).
set -euo pipefail
title=$1 report=$2 intro=$3
number=$(gh issue list --state open --limit 100 --json number,title --jq ".[] | select(.title == \"$title\") | .number" | head -1)
if [[ -s $report ]]; then
  body=$(printf '%s\n\n%s\n\n_Checked %s by the weekly workflow._\n' "$intro" "$(cat "$report")" "$(date -u +%Y-%m-%d)")
  if [[ -n $number ]]; then gh issue edit "$number" --body "$body"; else gh issue create --title "$title" --body "$body"; fi
elif [[ -n $number ]]; then
  gh issue close "$number" --comment "Resolved: the check found nothing on $(date -u +%Y-%m-%d)."
fi
