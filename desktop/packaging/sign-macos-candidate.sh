#!/bin/bash
# Sign a CI-built app with the local Developer ID, without exporting its key.
# JDK 21 supports signing predefined app images:
# https://docs.oracle.com/en/java/javase/21/docs/specs/man/jpackage.html
set -euo pipefail
if [[ $# != 2 || ! -f "$1" || -e "$2" ]]; then
  echo "Usage: $0 unsigned-candidate.dmg new-signed-output.dmg" >&2
  exit 2
fi
: "${JAVA_HOME:?Set JAVA_HOME to a non-Homebrew JDK 21}"
: "${MAC_SIGN_ID:?Set MAC_SIGN_ID to the Developer ID name and team ID}"
script_dir=$(cd "$(dirname "$0")" && pwd)
input=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
mkdir -p "$(dirname "$2")"
output=$(cd "$(dirname "$2")" && pwd)/$(basename "$2")
scratch=$(mktemp -d "${TMPDIR:-/tmp}/pc110-sign.XXXXXX")
mounted=false
cleanup() {
  if [[ "$mounted" == true ]]; then hdiutil detach "$scratch/mount" -quiet || true; fi
  rm -rf "$scratch"
}
trap cleanup EXIT
mkdir "$scratch/mount" "$scratch/image"
# CI embeds this project's publisher-selected MIT license in the DMG.
PAGER=cat hdiutil attach "$input" -readonly -nobrowse -mountpoint "$scratch/mount" <<< 'y'
mounted=true
test -d "$scratch/mount/PC110 Atlas.app"
ditto "$scratch/mount/PC110 Atlas.app" "$scratch/image/PC110 Atlas.app"
hdiutil detach "$scratch/mount" -quiet
mounted=false
replacement_args=()
if [[ -n "${PC110_NATIVE_LIBRARY:-}" ]]; then
  replacement_args=(--pc110-native-library "$PC110_NATIVE_LIBRARY")
fi
python3 "$script_dir/sign-jar-natives.py" "$scratch/image/PC110 Atlas.app/Contents/app" \
  --identity "Developer ID Application: $MAC_SIGN_ID" "${replacement_args[@]}"
"$JAVA_HOME/bin/jpackage" --type app-image --app-image "$scratch/image/PC110 Atlas.app" \
  --mac-sign --mac-signing-key-user-name "$MAC_SIGN_ID" \
  --mac-entitlements "$script_dir/macos-entitlements.plist"
codesign --verify --deep --strict --verbose=2 "$scratch/image/PC110 Atlas.app"
codesign --display --verbose=2 "$scratch/image/PC110 Atlas.app"
ln -s /Applications "$scratch/image/Applications"
hdiutil create -volname 'PC110 Atlas' -srcfolder "$scratch/image" -fs HFS+ -format UDZO "$output" -quiet
codesign --force --timestamp --sign "Developer ID Application: $MAC_SIGN_ID" "$output"
codesign --verify --strict --verbose=2 "$output"
echo "Signed candidate: $output"
echo 'Notarization and stapling are still required before public macOS release.'
