# Distribution validation, September 14, 2026

| Check | Result |
| --- | --- |
| macOS arm64 DMG build with Temurin JDK 21 | Passed |
| Packaged macOS launcher: JNI, Skia, resources, disposable media import | Passed |
| Desktop unit tests on macOS and Ubuntu arm64 | Passed |
| Ubuntu 24.04 arm64 DEB and RPM builds | Passed |
| DEB installation with APT and installed launcher smoke test | Passed |
| RPM installation with DNF on Fedora 44 arm64 and launcher smoke test | Passed |
| Snapcraft arm64 build, strict installation, confined launcher smoke test | Passed |
| Signed APT metadata accepted by APT, architecture indexes, RPM signature verification, tamper rejection | Passed with disposable test packages and a temporary signing key |
| Release manifest and checksum tests | 5 passed |
| GitHub Actions workflow validation with actionlint | Passed |
| Unix frontend build and X11 tests on Linux x86_64 at 8-, 16-, and 24-bit depth | Passed |
| Portable core synthetic BIOS boot on emulated big-endian MIPS Linux | Passed |
| Actual IRIX 6.5 / SGI workstation execution | Not yet tested |
| Windows installer / Chocolatey execution, macOS Intel, and Linux x64 native packages | Defined in CI; not executed in this validation |
| Developer ID signing, notarization, public repositories, and store submissions | Require publisher credentials; not performed |

The Snap was executed in a systemd service because the local VM's SSH session
cgroup was not accepted by snapd. Strict confinement remained enabled.
Snapcraft reports unused Java libraries that are loaded dynamically, and the
unset application license metadata. The Java libraries are retained; the
publisher must supply the correct license declaration before submission.

Testing found that jpackage did not infer RPM dependencies when building on
Ubuntu. The Gradle packaging tasks now explicitly declare the required
graphics, font, audio, C++, and X11 runtime dependencies. The updated package
was installed and tested on Fedora. DEBs also explicitly require EGL and fonts.

The initial x86 VM validation stopped after its Ubuntu Java runtime crashed
under QEMU TCG, before application compilation. Native arm64 Linux validation
with Temurin completed successfully. No app workaround for that VM-specific
crash was added.

Four Linux store screenshots are saved in `snap/screenshots/`. Local test
installers and the Unix source archive are under
`build/distribution-validation/packages/`. The macOS test DMG is unsigned;
release CI requires signing and notarization before publishing it.
