# Pi-Apps candidate, PC110 Atlas 1.0.1

The ARM64 review candidate includes the Pi 5 fixes and the Linux QEMU backend.
It is rebuilt on Ubuntu 22.04 to support the older library ABI used by Bookworm
and Jammy. It does not replace any published 1.0.0 artifact. Pi-Apps acceptance
is pending; see [submission details](SUBMISSION.md) and [hardware evidence](HARDWARE-TEST.md).

## Compatibility

The installer accepts 64-bit Raspberry Pi OS / Debian Bookworm and Trixie,
plus Ubuntu 22.04 Jammy, 24.04 Noble and 26.04 Resolute. One unchanged DEB passed
installation, native/QEMU smoke, four UI renders, reinstall, purge and synthetic
media preservation in clean native ARM64 containers for all five distributions.

Interactive testing used a Pi 5 Model B, 4 GB, Raspberry Pi OS Trixie, labwc
Wayland/Xwayland. Other Pi models, Switchroot and Jetson desktops are not
hardware-validated. Container tests do not prove every GPU, compositor, speaker
or guest application works. The upstream OS-image workflow is a separate gate.

32-bit ARM, Bullseye and older distributions are not supported. The app needs
GLIBC 2.35 or newer. Do not mix distribution repositories, force dependencies
or modify the user's OS to bypass this requirement. The installer fails before
downloading on an unsupported OS or architecture.

## Review release and safety

The 1.0.1 ARM64 review release is published. GitHub Actions is enabled for
the fork's required checks; unrelated workflows remain disabled. Upstream
image checks and public-artifact integration passed. The app is submitted in
[Pi-Apps PR #3051](https://github.com/Botspot/pi-apps/pull/3051), awaiting maintainer review.

- [ARM64 1.0.1 DEB](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.1/pc110-atlas-1.0.1-linux-arm64.deb)
- DEB SHA-256: `2890c907e7087532ff860c6aada02017913305e8701a13791936e8f80c053f5b`
- [Pi-Apps import ZIP](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.1/PC110-Atlas-Pi-Apps-1.0.1.zip)
- ZIP SHA-256: `c2dbf46f62e4d4a22fdbabb224a5f7381c37235da3b93ad86c0dc7853db61272`

The seven-file script-app uses `install_packages` only after a pinned HTTPS
download passes SHA-256 verification. Uninstall uses `purge_packages` and
preserves imported media/preferences. Temporary downloads are cleaned up. No
external APT repository or key is added. Java is bundled. The shortcut appears
in Education; the proposed Pi-Apps category is `Tools/Emulation`.

No IBM ROMs, Windows, DOS or PersonaWare are included. The boot demo is original
project content. The review release supplies exact modified QEMU source/build
inputs, SeaBIOS sources/notices and matching Temurin source/build
scripts. Private guest media and screenshots are never public test artifacts.
Linux imports remain under `$XDG_DATA_HOME/pc110-atlas/media`, defaulting to
`~/.local/share/pc110-atlas/media`.

## Validation commands

```sh
python3 -m unittest discover -s desktop/packaging/tests -p test_pi_apps.py -v
shellcheck desktop/packaging/pi-apps/PC110\ Atlas/install-64 \
  desktop/packaging/pi-apps/PC110\ Atlas/uninstall \
  desktop/packaging/pi-apps/test-container.sh \
  desktop/packaging/pi-apps/test-session.sh
python3 desktop/packaging/package-pi-apps.py \
  --deb /path/to/pc110-atlas-1.0.1-linux-arm64.deb \
  --output /path/to/PC110-Atlas-Pi-Apps-1.0.1.zip
```

The ZIP builder verifies the DEB checksum, allows only seven files, gives scripts
mode 775 and refuses to overwrite a ZIP. Nine installer/ZIP tests cover guards,
checksum failures, cleanup, dependency helpers and deterministic packaging.

The manual **Pi-Apps candidate verification** workflow uses the real upstream
helpers in disposable ARM64 containers for all five distributions. It exercises
the public artifact, packaged native/QEMU smoke, four UI exports, reinstall,
uninstall, repeated uninstall and synthetic-media preservation. The helper is
pinned to `9cb5e7d21b4ec38421fd241856d1a7e106e546c0`. No personal media is mounted.

Upstream `test_build.yml` passed for all six selected ARM64 images. The workflow
URLs are in [SUBMISSION.md](SUBMISSION.md). It checks install/uninstall in actual
OS images, not interactive graphics. Do not run autoremove-based lifecycle
checks on a personal Pi with unrelated auto-removable packages.

The PR against upstream master includes exact test results and limits. Do not
claim catalog availability until maintainers accept it. Earlier 1.0.0 results
and failed test-harness attempts are retained as history in the hardware report.

References: [creating an app](https://pi-apps.io/wiki/development/Creating-an-app/),
[contributing](https://github.com/Botspot/pi-apps/blob/master/CONTRIBUTING.md).
