#!/bin/bash
# Paste the publisher key privately and send it directly to Actions secrets.
set -euo pipefail
set +x
repository=${DISTRIBUTION_REPOSITORY:-ahmadexp/homebrew-pc110-atlas}
if [[ ! -t 0 ]]; then
  echo 'Run this script in an interactive terminal.' >&2
  exit 2
fi
gh auth status >/dev/null
echo "Destination: $repository, GitHub Actions secret CHOCO_API_KEY"
echo 'Copy the publishing API key from your Chocolatey Community account.'
read -r -s -p 'Chocolatey API key (hidden): ' chocolatey_key
printf '\n'
if [[ -z "$chocolatey_key" ]]; then
  echo 'No API key was entered.' >&2
  exit 2
fi
trap 'unset chocolatey_key' EXIT
printf '%s' "$chocolatey_key" | gh secret set CHOCO_API_KEY \
  --app actions --repo "$repository"
unset chocolatey_key
echo 'The publishing key has been saved to GitHub Actions.'

