#!/bin/bash
# Integration harness ONLY for a disposable, network-enabled ARM64 container.
# /upstream is a read-only Pi-Apps checkout; /candidate is this directory.
# /results is a dedicated, empty output directory. No personal media is mounted.
set -eo pipefail
if [ "${PC110_DISPOSABLE_CONTAINER:-}" != 1 ] || [ ! -f /.dockerenv ] || [ "$(id -u)" != 0 ] || [ "$(uname -m)" != aarch64 ]; then
  echo 'Run only in an explicitly opted-in disposable ARM64 Docker container.' >&2
  exit 1
fi
test -f /upstream/api
test -f '/candidate/PC110 Atlas/install-64'
test -d /results
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends sudo systemd-sysv ca-certificates wget \
  curl git lsb-release procps bc jq apt-utils binutils xz-utils gzip xauth xvfb \
  fonts-dejavu-core locales
localedef -i en_US -f UTF-8 en_US.UTF-8
useradd --create-home --shell /bin/bash pc110test
printf 'pc110test ALL=(ALL) NOPASSWD: ALL\n' > /etc/sudoers.d/pc110test
chmod 440 /etc/sudoers.d/pc110test
cp -a /upstream /home/pc110test/pi-apps
cp -a '/candidate/PC110 Atlas' '/home/pc110test/pi-apps/apps/PC110 Atlas'
chown -R pc110test:pc110test /home/pc110test/pi-apps
install -d -o pc110test /var/cache/pi-apps
install -d /usr/share/desktop-directories /usr/share/applications
# Reopening Docker's root-owned stderr pipe as the unprivileged user can fail.
# A user-owned log also retains full dpkg diagnostics if an integration fails.
result=0
runuser -u pc110test -- bash -c 'set -o pipefail; bash /candidate/test-session.sh 2>&1 | tee /home/pc110test/session.log' || result=$?
cp /home/pc110test/session.log /results/session.log
[ "$result" = 0 ] || exit "$result"
cp -a /home/pc110test/screenshots /results/
printf 'PC110 Pi-Apps container integration passed on %s / %s\n' "$(lsb_release -cs)" "$(uname -m)"
