# Windows 1.0.3

October 17, 2026. Standalone Windows x64 installers now include direct screen
pointing and the current iPhone keyboard layout, including the corrected Up key.

- Point at the emulated LCD using the host mouse or touch. The pictured
  TrackPoint remains available; the next screen interaction takes over again.
- Recognized PersonaWare and Windows FAT12/FAT16 working disks receive the
  matching pointer setup with a recoverable backup. Imported originals are
  preserved. Unsupported formats retain relative input.
- Import a complete media ZIP, Japanese font ROM, compatible raw disks up to
  4 GiB, or a custom PNG shell. Explore the PCB in 3D.
- The bundled native runtime supports guest audio and persistent writes to
  private disk copies. Proprietary firmware and operating-system media are
  not included.

The MSI and EXE were built and tested locally on Windows 11 x64. See
[installer validation](QA-WINDOWS-1.0.3.md) for test coverage and checksums.
They are not Authenticode signed, so Windows may show an unknown-publisher
warning. Shut down the guest and back up imported media before updating.

The matching Chocolatey NUPKG also passed installation from the public,
checksum-pinned MSI, installed-app tests and automatic removal. It is available
with the GitHub release for local installation. Community Repository 1.0.0
remains the approved version until the 1.0.3 submission is accepted and reviewed.

Windows 95 remains experimental. Known guest stability and text-layout issues
remain; exact pointing is not guaranteed for every imported disk.

These installers do not update Microsoft Store, Linux, mobile or headset
editions. Mac/Homebrew 1.0.3 is published separately in the same release.
