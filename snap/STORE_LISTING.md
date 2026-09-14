# Snap Store listing

Name: `pc110-atlas` (registered to `ahmadexp`)

Snap ID: `agfCUkEwmIKQZEpG7BzVAlP7maoZEimj`

Published on September 14, 2026: [PC110 Atlas in the Snap Store](https://snapcraft.io/pc110-atlas).
Version 1.0.0 is on stable and edge for amd64 (revision 1) and arm64 (revision 2).
The title, Education category, description, license, website, issue link, icon,
and four Ubuntu screenshots have been saved and checked on the public page.

Title: PC110 Atlas

Summary: Explore and emulate the IBM Palm Top PC 110

Category: Education

Website: https://github.com/ahmadexp/homebrew-pc110-atlas

Support: https://github.com/ahmadexp/homebrew-pc110-atlas/issues

Icon: `snap/store-icon.png`, 512 by 512 pixels and 253,590 bytes. It is a
lossless recompression of the desktop icon, verified to have identical RGBA
pixels, and fits the Store's 256 KB upload limit.

Screenshots: `snap/screenshots/`, four 1600 by 1000 PNGs rendered from the
installed Linux package with an empty media repository. Provenance is recorded
alongside them. All four are published in the store listing.

## Description

Explore the IBM Palm Top PC 110 through an interactive hardware reference,
historical archive, and portable emulator.

Browse PCB layer stacks and schematics, explore the computer's history, and
use keyboard and mouse input with the emulated display. Import your own
legally obtained PC110 BIOS and raw disk images to run the emulator. IBM
firmware, PersonaWare, DOS, and Windows are not included.

Imported media stays on your computer. A Java runtime and the native portable
emulator are included, so no separate Java installation is required.

This is an independent project and is not affiliated with or endorsed by IBM.

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
workflows. The first upload completed in publishing run `34867075816`.
Store installation and launcher tests passed on Ubuntu arm64, including the
change from edge to stable. Revisions were then confirmed for both architectures.
Future releases should refresh the listing and repeat relevant functional checks.
