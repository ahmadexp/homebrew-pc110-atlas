# Desktop media packages and custom shells

These features are included in Mac/Homebrew 1.0.2. Older Homebrew 1.0.0
installers do not contain them. Other distribution channels update separately.

## Import everything from one ZIP

Power off the guest and select **Run > Personal media > Import ZIP package**.
Use your own legally obtained files, with the same layout as the iPhone edition:

```text
Firmware/
  pc110_bios.bin
  MSM538032E@SOP44.BIN
  M38223E4HP@QFP80.BIN
  M38813E4HP@QFP64.bin
Boot Media/
  Personaware.img
  SecondHDD.img
Customization/
  console-background.png
  console-overlay.png
```

Only BIOS and `Personaware.img` (HDD-1) are required. Font, MCU dumps, HDD-2,
and artwork are optional. An enclosing folder and case differences are accepted.
Existing desktop slot names (`PC110-BIOS.rom`, `PC110-FONT.rom`,
`PC110-POWER.bin`, `PC110-KEYBOARD.bin`, `HDD-1.img`, `HDD-2.img`) also work.
If two entries map to the same slot, the whole import is rejected.

The BIOS must be exactly 256 KiB. The font dump must be
exactly 1 MiB with a FONT header. Power and keyboard MCU dumps must be exactly
16,254 and 16,255 bytes respectively. The portable core loads both MCU dumps;
Full-emulator editions retain them in the vault but use their existing device emulation.

The archive is fully checked before replacement. ZIP CRCs, file sizes, disk
alignment, artwork dimensions and unsafe paths are checked. At most 1,024
entries are allowed. Unknown files are skipped, never executed or installed.
There is no automatic firmware download or guest boot.

Original source files are unchanged. Imports go into the app's private `media`
directory. Previous contents are retained in the adjacent
`media-backups/package-<identifier>` directory. A media-only ZIP preserves
omitted optional files. Replacing a disk resets that disk's saved CMOS
settings; the previous settings remain in the backup. Interrupted directory
replacement is recovered when the app next starts. To restore manually, close
the app, keep a copy of the current `media` folder, then restore the desired
backup as `media`.

## Raw disk size

Each disk can contain up to **4 GiB (4,294,967,296 bytes)**, in complete 512-byte
sectors. This applies to individual imports and ZIPs, and to both desktop
backends. ZIP64 archives are supported. A full package's compressed size is
limited to two maximum-size disks plus 64 MiB. Allow enough free storage for
the extracted set and retained backups, not just the compressed archive.

On the portable core, disks larger than 512 MiB use a private, demand-paged
file mapping. They are not read entirely into a heap allocation, and their MBR
and sector layout are preserved. Smaller images retain the existing PersonaWare
compatibility loader. This does not add persistent guest disk writes to the
portable core. The full emulator continues to write to its private imported disk copy.

Guest BIOS geometry, partition format and operating-system limitations still
apply. A larger accepted image is not a guarantee that every guest OS will boot.
Mac/Homebrew 1.0.2 includes the [Mac emulator](MACOS-EMULATION.md) with guest
audio and experimental Windows 95 support. Use the documented Windows
environment and matching guest drivers. Windows 95 is not fully validated.

Only raw IMG disks are accepted. QCOW2, VHD/VHDX and VMDK containers must be
converted to raw first. Renaming a container to `.img` does not convert it.

## Custom shell artwork

Use **Import custom shell ZIP** for artwork only, or include `Customization` in
a full media ZIP. Provide a background, an overlay, or both. Each must be a PNG
of exactly **1086 x 1448 pixels**, at most 20 MiB. Artwork-only ZIPs have a 40 MiB
compressed limit. Image dimensions are checked before full decoding.

The overlay is placed above the background. If only an overlay is provided,
the bundled PC110 console is the background. The live LCD is drawn above both
images at the same reference position as iPhone (221,100; 675 x 481), so opaque
artwork cannot obscure the display or intercept guest input. Importing artwork
replaces the complete artwork set; the previous set remains in the ZIP backup.

The console includes the interactive JIS keyboard, TrackPoint, mouse buttons
and PersonaWare pen pad. Custom artwork uses the same control positions as the
bundled console and iPhone edition. It is not a free-standing 3D laptop or a
replacement terminal. Your computer's keyboard and mouse also control the guest.
The console works in the Run preview and full screen.
**Display only / Show PC110 console** switches presentation without deleting
the imported artwork. Full screen retains its visible **Exit full screen** control.

## 3D PCB explorer

Select **Hardware > 3D PCB** for Mainboard, PSU, Modem, 16 MB RAM or Docking
Station. Drag horizontally to rotate and vertically to orbit. Scroll or use
the Zoom slider. Tilt can pass through the edge-on view to either underside.
Use layer visibility, X-ray layers, Layer spacing, 2D view and Reset view to
inspect the stack. This is an interactive 3D projection of registered board
layers, not a free-standing 3D laptop model.

All layers share a physical board coordinate frame. Underside assembly artwork
is mirrored in texture space only. Copper exports are already in board space.
Occlusion order reverses below the board. Mainboard copper is clipped to the
KiCad outline, while assembly overhangs retain their original transparency.
