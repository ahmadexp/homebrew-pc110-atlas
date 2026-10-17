# Mac 1.0.3

October 17, 2026. This update covers the standalone Mac/Homebrew edition for
Intel and Apple silicon, separately from the Mac App Store app.

## Changes

- Point directly at the emulated screen with the host mouse. Screen interaction
  takes over automatically after using the pictured TrackPoint.
- Recognized PersonaWare and Windows FAT12/FAT16 working disks receive the
  matching direct-pointer setup, with a recoverable backup. Original imported
  files are unchanged. Unsupported guest formats retain relative input.
- Updated iPhone keyboard layout, with Up directly above Down and separate from
  the neighboring Ro and Right Shift keys. Pictured and physical Up input use
  the same guest key code.
- Release checks reject a bundled runtime whose recorded source inputs are
  older than the current pointer implementation.

Media ZIP import, Japanese font ROMs, custom PNG shells, 4 GiB raw disks,
the 3D PCB viewer and guest audio remain available. No proprietary firmware,
operating systems or personal media are included.

## Install or update

Update an existing installation with:

```sh
brew update
brew upgrade --cask pc110-atlas
```

For a new installation:

```sh
brew install --cask ahmadexp/pc110-atlas/pc110-atlas
```

Shut down the guest and back up imported media before updating. Ordinary
updates and uninstalls preserve media; Homebrew's `--zap` removes it.

## Validation and limits

See [the 1.0.3 validation record](QA-MACOS-1.0.3.md). Native builds and tests run
on local Intel and Apple silicon machines. Both installers are Developer ID
signed, Apple notarized and stapled, and passed verification on their native
architecture before publication.

Windows 95 remains experimental. An intermittent VMM crash and historical DOS
text-layout issue are not declared fixed by this update. Exact pointing requires
a compatible guest driver; it is not guaranteed for every imported disk. Previous
[guest-validation limits](QA-MACOS-1.0.2.md#guest-and-feature-limits) still apply.

This Mac release does not update the Windows/Chocolatey, Linux, mobile, headset
or store editions. Corresponding runtime, dependency and firmware sources are
provided with the release, alongside the component notices.
