# PC110 Atlas for Linux, Windows, and macOS

The desktop port brings the Atlas interface, portable PC110 emulator, personal
media import, interactive PCB layers, vector schematics, archive, and credits
to Linux, Windows, and macOS from one Compose Desktop codebase. It does not contain IBM
firmware, PersonaWare, DOS, Windows, or any other operating-system media.

Mac/Homebrew and standalone Windows 1.0.3 are published, with direct pointing
and the corrected Up-key layout. All builds and installer tests ran locally.
See the [Mac release notes](RELEASE-MACOS-1.0.3.md),
[Windows release notes](RELEASE-WINDOWS-1.0.3.md),
[Mac validation](QA-MACOS-1.0.3.md) and [Windows validation](QA-WINDOWS-1.0.3.md).
The tested Chocolatey 1.0.3 package is available on GitHub; Community submission
is pending. Linux and other platform channels are unchanged by this release.

## Run from source

The build commands below require the application source checkout. The public
Homebrew/download repository contains distribution tooling and release source
attachments, not the complete application checkout. Use the DMGs or Homebrew
for normal installation.

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
python3 desktop/qemu/build-macos.py desktop/build/qemu-macos
python3 desktop/qemu/package-macos.py desktop/build/qemu-macos desktop/build/qemu-runtime-macos-arm64
./android/gradlew -p desktop packageDmg -PrequireMacQemu=true
```

Use `qemu-runtime-macos-x64` on Intel. See [Mac emulation](MACOS-EMULATION.md)
for the native build dependencies, Windows 95 setup and validation limits.

Packages are written below `desktop/build/compose/binaries/main/`. Packaging
must run on the target operating system. The repository workflow builds both
platforms and preserves its packages for release validation. The desktop release
version comes from `packaging/version.txt`. See [distribution setup](DISTRIBUTION.md)
for Snap Store, signed APT/YUM repositories, Chocolatey, Homebrew, and release
signing. Mac/Homebrew 1.0.2 bundles the full emulator; older Homebrew 1.0.0 installers use the
portable core. The SwiftUI Mac Catalyst edition remains a separate target.
See [Mac 1.0.2 release notes](RELEASE-1.0.2.md) and
[signed-installer validation](QA-MACOS-1.0.2.md).

The [Pi-Apps 1.0.1 ARM64 review release](packaging/pi-apps/README.md) includes
the [Linux emulator](LINUX_QEMU.md), Swing media import, resizable PCB
layers, Wayland resizing and built-in offline schematics. It resolves the
reproduced Pi 5 failures of the original 1.0.0 portable package. Original and
English PersonaWare boot and interaction were tested with private media copies.
The rebuilt 1.0.1 DEB passes clean-container installation, native/emulator smoke,
graphics exports and lifecycle checks on Bookworm, Trixie, Jammy, Noble and
Resolute, plus packaged smoke on the Pi 5. Ubuntu 22.04 is the build baseline;
32-bit ARM is unsupported. Non-Mac 1.0.0 release channels are unchanged by the
Mac 1.0.2 update.
See [submission status](packaging/pi-apps/SUBMISSION.md) and the exact
[hardware evidence and limits](packaging/pi-apps/HARDWARE-TEST.md).

## Personal media

Use the Run tab to import a legally obtained PC110 BIOS and a raw disk image.
The current source supports raw disks up to 4 GiB, the optional Japanese font
ROM, iPhone-layout media ZIPs, and custom shell artwork, including macOS.
These improvements are included in Mac/Homebrew 1.0.2, not the older 1.0.0 package.
See [media packages and custom shells](MEDIA-PACKAGES.md),
[desktop feature validation](QA-DESKTOP-MEDIA-PCB.md), and
[font import validation](QA-FONT-ROM.md) for details and release checks.

To add it, power off the guest, then open **Run > Personal media** and click
**Japanese font ROM (optional)** (the row says **Choose a file** before import).
Select your own `MSM538032E@SOP44.BIN` dump, exactly
1 MiB (1,048,576 bytes). Renaming the source file is not required. The importer
checks the ROM size and FONT header, copies it privately as `PC110-FONT.rom`, and
leaves the original unchanged. Power on again to load it; it remains available
after Reset and app relaunch. If the ROM cannot be loaded, boot reports a font
ROM error instead of silently omitting it. The ROM is optional and is not bundled
or downloaded by the app. Invalid replacements preserve the previous import.

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
- The pictured JIS keyboard, TrackPoint, mouse buttons and PersonaWare pen pad
  are interactive. Shift, Ctrl, Alt and Fn are one-shot on-screen modifiers;
  lock keys stay active until toggled again.
- **Display only / Show PC110 console** changes presentation without replacing
  media or custom artwork. **Pause / Resume** temporarily suspends the guest.
- The standard PC keyboard, function keys, arrows, navigation keys, and common
  punctuation are passed to the guest through BIOS key values.
- Host pointer movement over the LCD automatically aligns the guest cursor.
  Primary, secondary, and middle buttons reach the guest after positioning.
  TrackPoint control remains relative; the next LCD interaction restores direct
  pointing. No input-mode setting is needed. The pen pad remains independent.
  See the [1.0.3 notes](RELEASE-MACOS-1.0.3.md) for guest setup and limits.
- Full screen keeps a close control visible in the top-right corner.
- Open **Hardware > 3D PCB** beside any of the five boards. Drag to orbit and
  rotate, scroll to zoom, or use the camera sliders. Layer spacing, individual
  visibility, X-ray transparency, underside inspection, 2D view and Reset view
  are available. Assembly textures and copper share the corrected board frame.
- Hardware schematics open in the built-in offline PDF viewer in Mac/Homebrew 1.0.2.
  The published portable 1.0.0 package still uses the system PDF viewer.

The [Windows Store candidate](WINDOWS_QEMU.md) builds a native Windows emulator
backend with the shared PC110 device models, display, audio, input, and a live
open-source boot demo. This backend is bundled by the Windows Store
pipeline. Native Linux packages can bundle the matching ARM64/x86-64 runtime
using the [Linux build instructions](LINUX_QEMU.md); the Linux package workflow
now requires it. The [Mac build](MACOS-EMULATION.md) also bundles the full emulator for Windows 95
and guest audio, with persistent writes to the imported disk copy.
Source builds and other editions retain the portable core when
no matching runtime is bundled. See the [Store release checklist](MICROSOFT_STORE.md)
for the actual validation and submission status.
