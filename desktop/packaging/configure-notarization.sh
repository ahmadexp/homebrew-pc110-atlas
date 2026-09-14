#!/bin/bash
# Store a validated notarization login locally without exposing its password.
set -euo pipefail
set +x
profile=${NOTARY_KEYCHAIN_PROFILE:-pc110-atlas-publishing}
team=${APPLE_TEAM_ID:-TWFK4FAG36}
if [[ $(uname -s) != Darwin || ! -t 0 ]]; then
  echo 'Run this script in an interactive macOS terminal.' >&2
  exit 2
fi
echo "Notarization profile: $profile"
echo "Apple Developer team: $team"
echo 'Use the Apple Account associated with this developer team.'
echo 'Generate an app-specific password at account.apple.com first.'
read -r -p 'Apple Account email: ' notary_account
if [[ -z "$notary_account" ]]; then
  echo 'An Apple Account email is required.' >&2
  exit 2
fi
# Omitting --password makes notarytool show its own secure password prompt.
xcrun notarytool store-credentials "$profile" \
  --apple-id "$notary_account" --team-id "$team"
echo "Validated notarization credentials are stored in Keychain as $profile."

