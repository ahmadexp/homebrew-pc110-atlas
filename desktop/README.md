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
- Hardware schematics open in the operating system's PDF viewer.

The production QEMU backend used by the iPhone app remains a future desktop
milestone. The initial desktop release deliberately uses the portable core that
also serves as the Android fallback.
