# Snap Store listing

Name: `pc110-atlas` (registered to `ahmadexp`)

Snap ID: `agfCUkEwmIKQZEpG7BzVAlP7maoZEimj`

Publisher agreement accepted on September 14, 2026. Package upload and listing
submission are pending. The Ubuntu One account needs a username before the
listing editor can be accessed.

Title: PC110 Atlas

Summary: Explore and emulate the IBM Palm Top PC 110

Category: Education

Website: https://github.com/ahmadexp/homebrew-pc110-atlas

Support: https://github.com/ahmadexp/homebrew-pc110-atlas/issues

Icon: `desktop/packaging/pc110-atlas.png`, 512 by 512 pixels

Screenshots: `snap/screenshots/`, four 1600 by 1000 PNGs rendered from the
installed Linux package with an empty media repository. Provenance is recorded
alongside them. They are ready for upload to the store dashboard.

## Description

Explore the IBM Palm Top PC 110 through an interactive hardware reference,
historical archive, and portable emulator.

Browse PCB layer stacks and schematics, explore the computer's history, and
use keyboard and mouse input with the emulated display. Import your own
legally obtained PC110 BIOS and raw disk images to run the emulator. IBM
firmware, PersonaWare, DOS, and Windows are not included.

Imported media stays on your computer. A Java runtime and the native portable
emulator are included, so no separate Java installation is required.

## Reviewer notes

Discover, Hardware, Archive, and Credits can be explored without importing
media. The Run section requires the user's own BIOS and raw disk image.
Raw disks must contain complete 512-byte sectors and be no larger than 512 MB.

The strictly confined snap requests home access for user-selected media and
uses snap-private storage for imported copies. The optional removable-media
interface enables imports from removable drives. Desktop portals open
schematics and project links in the user's chosen applications.

This desktop edition uses the portable core. It does not claim feature parity
with the Apple and Android QEMU editions. The project is independent of IBM.

## Submission assets and checks

- Confirm the registered publisher profile and licensing fields.
- Upload the icon and the prepared Discover, Hardware, Archive, and Run
  screenshots in the Snapcraft dashboard. Refresh these images after UI changes.
- Publish to edge and test BIOS import, disk import, keyboard, mouse,
  schematics, removable media, and persistence across refreshes.
- Promote to stable after store acceptance and functional validation.

The build, upload, and channel selection are automated in the desktop
workflows. Listing fields, screenshots, and store review still require completion in
the publishing account.
