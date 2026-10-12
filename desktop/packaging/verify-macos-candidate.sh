#!/bin/bash
# Verify the exact signed, stapled installer on its native architecture.
set -euo pipefail
if [[ $# != 3 || ! -f "$1" || -e "$2" || ! "$3" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo 'Usage: verify-macos-candidate.sh installer.dmg new-evidence-directory version' >&2
  exit 2
fi
installer=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
mkdir -p "$2"
evidence=$(cd "$2" && pwd)
expected_version=$3
mount_point=$(mktemp -d)
mounted=false
cleanup() {
  if [[ "$mounted" == true ]]; then hdiutil detach "$mount_point" -quiet || true; fi
  rmdir "$mount_point" || true
}
trap cleanup EXIT
codesign --verify --strict --verbose=2 "$installer" 2>&1 | tee "$evidence/dmg-signature.txt"
xcrun stapler validate "$installer" 2>&1 | tee "$evidence/stapler.txt"
spctl --assess --type open --context context:primary-signature --verbose=2 "$installer" 2>&1 | tee "$evidence/gatekeeper-dmg.txt"
PAGER=cat hdiutil attach "$installer" -readonly -nobrowse -mountpoint "$mount_point" <<< 'y'
mounted=true
app="$mount_point/PC110 Atlas.app"
launcher="$app/Contents/MacOS/PC110 Atlas"
test "$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$app/Contents/Info.plist")" = "$expected_version"
test "$(lipo -archs "$launcher")" = "$(uname -m)"
codesign --verify --deep --strict --verbose=2 "$app" 2>&1 | tee "$evidence/app-signature.txt"
codesign --display --verbose=4 "$app" 2>&1 | tee "$evidence/app-identity.txt"
spctl --assess --type execute --verbose=2 "$app" 2>&1 | tee "$evidence/gatekeeper-app.txt"
"$launcher" --smoke-test > "$evidence/native-smoke.txt" 2>&1
"$launcher" --qemu-smoke-test "$evidence/qemu" > "$evidence/qemu-smoke.txt" 2>&1
/usr/bin/shasum -a 256 "$installer" | tee "$evidence/SHA256SUMS"
echo "Verified signed $expected_version installer on $(uname -m)"
