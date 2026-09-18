#!/bin/bash
# Called by test-container.sh; deliberately does not enable nounset in upstream api.
# Pi-Apps provides the sourced files and exported OS variables at runtime.
# shellcheck disable=SC1091,SC2154
set -eo pipefail
if [ "${PC110_DISPOSABLE_CONTAINER:-}" != 1 ] || [ ! -f /.dockerenv ] || [ "$(id -un)" != pc110test ]; then
  echo 'This test session belongs in the disposable integration container.' >&2
  exit 1
fi
export DIRECTORY=/home/pc110test/pi-apps
export app='PC110 Atlas'
mkdir -p "$DIRECTORY/data/settings" "$DIRECTORY/data/status" "$DIRECTORY/logs"
# shellcheck disable=SC1091
source "$DIRECTORY/api"
test "$arch" = 64
printf 'Pi-Apps OS detection: %s %s %s; arch=%s\n' "$__os_id" "$__os_release" "$__os_codename" "$arch"

# Simulated user data, never proprietary guest files. Check both data locations.
mkdir -p /home/pc110test/.local/share/pc110-atlas/media /home/pc110test/custom-data/pc110-atlas/media
printf 'default user media sentinel\n' > /home/pc110test/.local/share/pc110-atlas/media/test-sentinel.txt
printf 'custom user media sentinel\n' > /home/pc110test/custom-data/pc110-atlas/media/test-sentinel.txt
sha256sum /home/pc110test/.local/share/pc110-atlas/media/test-sentinel.txt \
  /home/pc110test/custom-data/pc110-atlas/media/test-sentinel.txt > /home/pc110test/sentinels.sha256

( source "$DIRECTORY/apps/PC110 Atlas/install-64" )
expected_version=$(sed -n 's/^version=//p' "$DIRECTORY/apps/PC110 Atlas/install-64")
test "$(dpkg-query -W -f='${Version}' pc110-atlas)" = "$expected_version"
test "$(dpkg-query -W -f='${Architecture}' pc110-atlas)" = arm64
launcher="$(dpkg-query -L pc110-atlas | sed -n '\|/bin/PC110 Atlas$|p')"
test -x "$launcher"
"$launcher" --smoke-test
"$launcher" --qemu-smoke-test /home/pc110test/qemu-smoke
xvfb-run -a -s '-screen 0 1600x1000x24' "$launcher" --export-store-screenshots /home/pc110test/screenshots
test "$(find /home/pc110test/screenshots -name '*.png' | wc -l)" = 4

# Reinstall through the real helper, exercising its dependency-accounting path.
( source "$DIRECTORY/apps/PC110 Atlas/install-64" )
"$launcher" --smoke-test
( source "$DIRECTORY/apps/PC110 Atlas/uninstall" )
test ! -e "$launcher"
sha256sum --check /home/pc110test/sentinels.sha256
# Uninstall again must be safe, including when the helper package is absent.
( source "$DIRECTORY/apps/PC110 Atlas/uninstall" )
sha256sum --check /home/pc110test/sentinels.sha256
printf 'Install, packaged smoke, UI rendering, reinstall, uninstall, and media preservation passed.\n'
