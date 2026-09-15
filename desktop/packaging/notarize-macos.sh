#!/bin/bash
# Sign through Compose first; this script submits and staples the resulting DMG.
set -euo pipefail
if [[ $# -ne 1 || ! -f "$1" ]]; then
  echo "Usage: $0 path/to/PC110-Atlas.dmg" >&2
  exit 2
fi
credentials=()
if [[ -n "${NOTARY_KEYCHAIN_PROFILE:-}" ]]; then
  credentials=(--keychain-profile "$NOTARY_KEYCHAIN_PROFILE")
else
  : "${APPLE_ID:?Set APPLE_ID or NOTARY_KEYCHAIN_PROFILE}"
  : "${APPLE_APP_PASSWORD:?Set APPLE_APP_PASSWORD}"
  : "${APPLE_TEAM_ID:?Set APPLE_TEAM_ID}"
  credentials=(--apple-id "$APPLE_ID" --password "$APPLE_APP_PASSWORD" --team-id "$APPLE_TEAM_ID")
fi
xcrun notarytool submit "$1" "${credentials[@]}" --wait --output-format json \
  > "$1.notarization.json"
python3 - "$1.notarization.json" <<'PY'
import json, sys
with open(sys.argv[1]) as stream:
    result = json.load(stream)
if result.get('status') != 'Accepted':
    raise SystemExit(f"Notarization was not accepted: {result}")
PY
xcrun stapler staple "$1"
xcrun stapler validate "$1"
