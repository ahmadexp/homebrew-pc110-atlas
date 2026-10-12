# PC110 Atlas 1.0.2 for Mac

Standalone Mac/Homebrew update for Intel and Apple silicon, targeting macOS 12
or later. See the [release validation record](QA-MACOS-1.0.2.md) for the exact
installer checks and remaining compatibility limits.

## Changes

- Use the interactive PC110 console with the iPhone JIS key layout, TrackPoint,
  mouse buttons and PersonaWare pen pad. Pause, resume, switch to display-only
  presentation, or use full screen with a visible exit button.
- Import an iPhone-layout ZIP containing your own PC110 firmware, raw disks
  and optional shell artwork. Individual file import remains available.
- Import the optional Japanese font ROM from Run > Personal media.
- Customize the emulator shell with compatible background and overlay PNGs.
- Import raw disks up to 4 GiB per disk. Guest filesystem limits still apply.
- Explore all five PCBs in 3D with layer spacing, visibility, underside views,
  X-ray transparency, rotation and zoom.
- Bundle a native Mac emulator with PC110 display and audio devices,
  guest audio transport and persistent writes to the app-private disk copy.
- Add experimental Windows 95 compatibility. A private installed image booted
  to a clean 640 x 480, 256-color desktop on Apple silicon.

## Important compatibility notes

Windows 95 is experimental, not fully validated. An intermittent VMM crash
occurred while rapidly switching Display Properties tabs. A DOS startup
text-layout artifact also remains. Long sessions, other guest applications,
and the full display/audio driver feature set have not been verified.

The Windows configuration is selected automatically for disks larger than
512 MiB. Smaller disks use the classic PC110/PersonaWare configuration. Import
your own compatible BIOS, installed operating system and matching drivers.
No IBM firmware, Microsoft software, PersonaWare or other proprietary media
is included or downloaded.

Before updating, shut down the guest and back up your imported media. Use the
Windows Start menu to shut down Windows before powering off the emulator.
Hardware Reset or Power off can leave the guest filesystem dirty and cause
ScanDisk on the next boot. Original imported source files are not modified.

This update is for the standalone Mac/Homebrew edition. It does not change
the Mac App Store, iPhone, Windows, Linux, Android or other store releases.

See [media ZIPs and shell artwork](MEDIA-PACKAGES.md),
[Mac emulation and validation limits](MACOS-EMULATION.md), and
[3D PCB and media QA](QA-DESKTOP-MEDIA-PCB.md).

## Install or update

Download the DMG matching your Mac from the
[1.0.2 release](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/tag/desktop-v1.0.2),
or update an existing Homebrew installation:

```sh
brew update
brew upgrade --cask pc110-atlas
```

For first-time installation, see the
[Homebrew instructions](https://github.com/ahmadexp/homebrew-pc110-atlas#install).
Keep Gatekeeper enabled. Both DMGs include their own Java and emulation runtimes;
you do not need a separate Java or emulator installation.
