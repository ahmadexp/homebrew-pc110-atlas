# PC110 Atlas for Linux, Windows, and macOS

The desktop port brings the Atlas interface, portable PC110 emulator, personal
media import, interactive PCB layers, vector schematics, archive, and credits
to Linux, Windows, and macOS from one Compose Desktop codebase. It does not contain IBM
firmware, PersonaWare, DOS, Windows, or any other operating-system media.

## Run from source

Install JDK 21 (Eclipse Temurin is recommended for native packaging) and CMake
3.22 or newer. From the repository root, run:

```sh
./android/gradlew -p desktop run
```

On Windows PowerShell or Command Prompt, use:

```powershell
android\gradlew.bat -p desktop run
```

The build compiles the C emulator core into `libpc110_desktop.so` on Linux or
`pc110_desktop.dll` on Windows, places it in the application resources, and
loads it from the packaged runtime. No separately installed emulator library is
needed.

## Create native packages

Linux:

```sh
./android/gradlew -p desktop packageDeb packageRpm
```

Windows:

```powershell
android\gradlew.bat -p desktop packageMsi packageExe
```

macOS:

```sh
./android/gradlew -p desktop packageDmg
```

Packages are written below `desktop/build/compose/binaries/main/`. Packaging
must run on the target operating system. The repository workflow builds both
platforms and publishes its packages as workflow artifacts. The desktop release
version comes from `packaging/version.txt`. See [distribution setup](DISTRIBUTION.md)
for Snap Store, signed APT/YUM repositories, Chocolatey, Homebrew, and release
signing. The Homebrew edition uses this portable core; the SwiftUI Mac Catalyst
edition remains a separate application target.

The [Pi-Apps 1.0.1 ARM64 review release](packaging/pi-apps/README.md) includes
the [Linux QEMU backend](LINUX_QEMU.md), Swing media import, resizable PCB
layers, Wayland resizing and built-in offline schematics. It resolves the
reproduced Pi 5 failures of the original 1.0.0 portable package. Original and
English PersonaWare boot and interaction were tested with private media copies.
The rebuilt 1.0.1 DEB passes clean-container installation, native/QEMU smoke,
graphics exports and lifecycle checks on Bookworm, Trixie, Jammy, Noble and
Resolute, plus packaged smoke on the Pi 5. Ubuntu 22.04 is the build baseline;
32-bit ARM is unsupported. Existing 1.0.0 release channels remain unchanged.
See [submission status](packaging/pi-apps/SUBMISSION.md) and the exact
[hardware evidence and limits](packaging/pi-apps/HARDWARE-TEST.md).

## Personal media

Use the Run tab to import a legally obtained PC110 BIOS and a raw disk image.
The desktop milestone supports raw disks up to 512 MB through the portable core.
Imported files are copied to:

- Linux: `$XDG_DATA_HOME/pc110-atlas/media`, or
  `~/.local/share/pc110-atlas/media` when `XDG_DATA_HOME` is unset
- Windows: `%APPDATA%\PC110 Atlas\media`
- macOS: `~/Library/Application Support/PC110 Atlas/media`
- Snap: `$SNAP_USER_COMMON/pc110-atlas/media`

HDD-1 and HDD-2 are independent boot choices. Select a disk, then use Reset or
power cycle the emulator to apply the selection. The source file chosen by the
user is never modified.

## Desktop controls

- Click the emulated display to give it keyboard focus.
- The standard PC keyboard, function keys, arrows, navigation keys, and common
  punctuation are passed to the guest through BIOS key values.
- Pointer movement and primary, secondary, and middle mouse buttons are passed
  to the guest.
- Full screen keeps a close control visible in the top-right corner.
- Hardware schematics open in the built-in offline PDF viewer in current source.
  The published portable 1.0.0 package still uses the system PDF viewer.

The [Windows Store candidate](WINDOWS_QEMU.md) builds a native Windows QEMU
backend with the shared PC110 device models, display, audio, input, and a live
open-source boot demo. This backend is bundled by the Windows QEMU/Store
pipeline. Native Linux packages can bundle the matching ARM64/x86-64 runtime
using the [Linux build instructions](LINUX_QEMU.md); the Linux package workflow
now requires it. Source builds and other editions retain the portable core when
no matching runtime is bundled. See the [Store release checklist](MICROSOFT_STORE.md)
for the actual validation and submission status.
