# PC110 Atlas for IRIX and X11 Unix

This is a lightweight native C99/Xlib edition targeting IRIX 6.5 on MIPS n32.
It provides a 640 by 480 emulated display, BIOS and disk loading, keyboard and
mouse input, pause/reset controls, and concise hardware/history reference
pages. It uses the same portable C emulator core as the modern desktop port.

It does not require Java, Kotlin, Compose, OpenGL, CMake, or a browser. The
modern desktop interface cannot be packaged directly for IRIX because its
runtime and graphics dependencies do not target that platform. This version
has no guest audio, 3D board explorer, embedded PDF viewer, or graphical file
picker. The hardware/archive pages are brief reference pages with source
addresses, rather than the complete modern Atlas content.

IRIX is a source build target, not a hardware-certified binary release. Linux
X11 checks and an emulated big-endian MIPS Linux core test are provided in
`.github/workflows/unix.yml`. Those tests do not establish IRIX ABI or runtime
compatibility. An actual SGI/IRIX build and boot test remains necessary.

## IRIX build

Install the IRIX 6.5 development headers and X11 development libraries, plus
a GCC toolchain with C99 support and GNU make. The
[SGUG software environment](https://github.com/sgidevnet/sgug-rse) supplies a
GCC toolchain for IRIX. Use its configured shell and library paths.

From the repository root, or an extracted Unix source release:

```sh
cd unix
/usr/sgug/bin/make -f irix.mk
/usr/sgug/bin/make -f irix.mk check
./build/pc110-atlas-unix
```

`irix.mk` targets n32 and MIPS III using `/usr/sgug/bin/gcc` and
`/usr/lib32/libX11`. Override paths if your compiler is installed elsewhere:

```sh
gmake -f irix.mk CC=/path/to/gcc
```

The compiler's runtime libraries must also support your machine's instruction
set. This recipe does not assert compatibility with every SGI CPU or every
version of the legacy MIPSpro compiler. Start with at least 128 MB of available
memory, plus space for the disk image loaded into memory. Larger disks may
exceed an older workstation's usable address space or physical memory.

After testing, install with the privileges required for your chosen prefix:

```sh
/usr/sgug/bin/make -f irix.mk install PREFIX=/usr/sgug
```

Use `DESTDIR=/temporary/staging` to stage an installation for a native archive
or package. Linux DEB/RPM files cannot be installed as IRIX binaries; build
this edition on IRIX with the matching ABI and runtime libraries.

## Other Unix systems

On Linux with GCC and X11 development headers:

```sh
make -C unix all check
unix/build/pc110-atlas-unix
```

BSD or other X11 systems may use the same Makefile with platform-specific
`CC`, `X11_CFLAGS`, and `X11_LIBS`. They have not been validated here. On macOS,
XQuartz is required for this frontend; the regular desktop app uses a native
macOS window and needs no X server.

## Personal media and controls

```sh
pc110-atlas-unix --bios /path/to/PC110.rom --disk /path/to/HDD.img
```

BIOS files must be at most 1 MB. Raw disks must contain whole 512-byte sectors
and be at most 512 MB. Media files are opened for reading; guest disk writes
stay in memory and are discarded on exit. No operating-system media or IBM
firmware is included. The core may also discover optional user-owned ROMs in
the working directory according to its existing ROM search rules.

Click tabs to switch pages. The Emulator tab receives guest keyboard and
pointer input. `Ctrl+Shift+P` pauses/resumes, `Ctrl+Shift+R` resets, and
`Ctrl+Shift+Q` quits. Closing the window also quits. Adjust older machines with
`--fps 10 --instructions 10000`; defaults are 15 frames/second and 40,000
emulated instructions per frame. These control workload, not an exact guest
clock rate.

The renderer selects a 24-bit or 16-bit TrueColor visual where available,
otherwise an 8-bit PseudoColor palette. It maps numeric ARGB channels through
the X visual masks and XPutPixel, avoiding little-endian byte assumptions on
big-endian MIPS. The window is fixed at 640 by 560 pixels.

## Verification and source release

`make check` boots an original synthetic test ROM that writes a known word
to guest memory and verifies the guest's little-endian layout, framebuffer,
and RGB conversion. It needs no firmware from the user. `--smoke-test` opens
an X window, draws a color test frame, and exits after three frames:

```sh
xvfb-run -a unix/build/pc110-atlas-unix --smoke-test
python3 desktop/packaging/package-unix-source.py --output desktop/build/release
```

The source archive contains this frontend and the portable core with a layout
that can be built on IRIX. It does not include Java binaries or private media.
Record the SGI model, IRIX version, compiler version, `file` output, `make check`
result, and graphical boot behavior when validating on hardware.

For an email-ready source testing kit with plain-text build instructions and
a report template, run:

```sh
python3 desktop/packaging/package-unix-source.py --test-kit --output build/irix-test-kit
```

Send the resulting `pc110-atlas-VERSION-irix-test-kit.tar.gz` attachment.
The recipient starts with `START-HERE.txt` inside the archive. A SHA-256
checksum file is generated alongside it. The kit requires compilation on
IRIX; it contains no precompiled IRIX executable.
