# Linux QEMU candidate

The Linux ARM64/x86-64 build can bundle the same PC110 QEMU devices and private
pipe transport as the Windows edition. This replaces the portable CPU execution
path in QEMU-enabled Linux packages. It does not repair the portable core itself.
The public Linux 1.0.0 artifact remains unchanged. The Pi-Apps 1.0.1 candidate
uses the older build baseline described below.

## Build

Use native Ubuntu 22.04 for the release baseline, JDK 21, CMake, GCC, Git, Ninja,
Python with venv and tomli, pkg-config, and the GLib, Pixman and zlib development packages.
Build ARM64 and x86-64 separately. The script refuses to overwrite a prepared
source tree or runtime; use a fresh checkout/build directory for a clean rebuild.
The runtime packager rejects QEMU executables requiring GLIBC newer than 2.35.
Building on 24.04 would silently exclude Bookworm and Jammy even if the package
names were changed, so rebuild both QEMU and the JNI library on 22.04.

```sh
bash desktop/qemu/build-linux.sh
python3 desktop/packaging/Test-Qemu-Pipe.py \
  desktop/build/qemu-runtime-linux-arm64 desktop/build/pipe-smoke
xvfb-run -a ./android/gradlew -p desktop test packageDeb packageRpm \
  -PrequireLinuxQemu=true -PdesktopVersion=1.0.1
```

For x86-64, use `qemu-runtime-linux-x64`. `PC110_QEMU_JOBS` controls build
parallelism (default 2). The shared pinned source revision and applied input
hashes are recorded in `PC110-DESKTOP-PROVENANCE.json`. The package includes
licenses, open-source SeaBIOS/VGA firmware, the original Atlas demo, and a
corresponding-source archive. It contains no IBM ROMs or proprietary guest disks.
GLib, Pixman, libffi, zlib and the C runtime use distribution packages, not copied private
libraries. The runtime loader validates the bundled hashes and makes only the
QEMU executable executable. It never searches PATH for an arbitrary QEMU binary.

## Behavior and regression checks

- Linux media selection uses Swing, avoiding the GTK/FreeType collision without
  changing system libraries or requiring `LD_PRELOAD`.
- PCB layers open in a resizable 900 x 700 dialog, with a 640 x 480 minimum and
  a bounded stack preview.
- Before AWT starts, Linux/Wayland launches fill in the process-local
  `_JAVA_AWT_WM_NONREPARENTING` flag when absent. Desktop-provided values are
  preserved. This also makes SSH launches resize correctly without changing
  labwc configuration, system libraries or global environment files.
- Schematics use the offline PDFBox viewer, with an eight-million-pixel render
  limit for high zoom. They do not depend on Evince or another external viewer.
- Desktop mouse buttons are translated to the portable core's zero-based API.
  QEMU keeps its existing separate translation.
- Numeric-keypad add, subtract, multiply and Enter are forwarded to the guest.
- Small personal images use the genuine 256 KiB PC110 BIOS, optional 1 MiB Kanji
  ROM, shared POST support and PC110 chipset. Larger disks use the existing
  Windows-compatible path. Guest networking remains disabled.
- Run the packaged `--qemu-smoke-test <new-output-directory>` to exercise actual
  guest text/graphics, keyboard, audio transport, reset, stop/restart, Unicode
  paths and read-only demo media. Audio transport is not proof of speaker output.

The real-device evidence and remaining submission gates are recorded in
[the Pi hardware report](packaging/pi-apps/HARDWARE-TEST.md). A successful demo
does not establish PersonaWare or Windows 95 compatibility. Personal-media
testing must use disposable copies and must not publish the media or captures.
Do not repoint the Pi-Apps installer until a new version has been validated and
published under a new immutable release URL.
