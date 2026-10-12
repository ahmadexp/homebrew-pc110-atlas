# Mac emulation and Windows 95

Mac/Homebrew 1.0.2 includes the full emulator. Windows 95 compatibility remains experimental.

The current desktop source can bundle a native interpreter on Apple
silicon and Intel Macs, with a macOS 12 deployment target. This is separate
from the SwiftUI Mac Catalyst edition. Homebrew 1.0.2 includes this backend;
the older 1.0.0 installers use only the portable core.

## Personal Windows 95 media

Import your legally obtained 256 KiB PC110 BIOS and installed raw Windows 95
disk from **Run > Personal media**, individually or in a media ZIP. No IBM
firmware, Microsoft software, activation material, or proprietary drivers are
bundled or downloaded. The BIOS must contain the supported PC110 C&T option ROM.

As on the other full-emulator editions, disks larger than 512 MiB select the Windows
environment automatically: a 486 CPU, 20 MiB RAM, strict SeaBIOS system firmware,
C&T F65535 graphics and ESS ES488-compatible audio. The original PC110 graphics
option ROM is extracted in memory from the imported BIOS. There is no machine
profile selector. Disks through 512 MiB retain the classic PC110/PersonaWare
environment, so small Windows installations are not covered by this selection
rule. The import limit is 4 GiB per raw disk, not a promise that every Windows
partition format or installation is supported.

Windows still needs its matching display and sound drivers. The basic VGA
desktop does not prove that 256-color C&T graphics or ESS playback is configured
inside a particular guest. See the validation limits below before advertising
driver or application compatibility.

The guest writes to the app-private imported disk, not the selected source
file. Shut Windows down from its Start menu before powering off the emulator.
Reset and Power off are hardware-style operations, not a Windows shutdown.
An already dirty disk can request ScanDisk; Tab selects a button and Enter
activates it. Canceling a scan can show a second confirmation before startup
continues. Let ScanDisk finish when possible.

## Runtime and build

The app runs only its bundled, SHA-256-verified executable and private libraries.
It does not require a separate emulator or Java installation, open a network
listener, or enable guest networking. Private pipes carry video, keyboard,
pointer input, and 44.1 kHz stereo PCM to the desktop host. A fresh emulator process
owns each boot. The TCG interpreter does not require JIT entitlements.

In the application source checkout, build natively on each architecture with Xcode command-line tools, Python 3.12
or later, Meson, Ninja, pkg-config, CMake, and the release JDK:

```sh
python3 desktop/qemu/build-macos.py desktop/build/qemu-macos
# Use macos-x64 on an Intel Mac, macos-arm64 on Apple silicon.
python3 desktop/qemu/package-macos.py desktop/build/qemu-macos desktop/build/qemu-runtime-macos-arm64
./android/gradlew -p desktop test packageDmg -PrequireMacQemu=true
```

For the standalone emulator corresponding-source archive attached to the release,
extract it and follow its included `README.txt` instead. It contains the patched
engine tree, dependency sources and native rebuild script without requiring the
complete application checkout.

Preparation pins the shared engine source and PC110 patches. GLib, libffi, PCRE2,
gettext and Pixman are built from checksum-pinned source for macOS 12 instead
of copying the host's Homebrew libraries. Packaging rejects unexpected external
dependencies, architecture mismatches and a newer minimum macOS requirement.
Each runtime includes notices, provenance, dependency archives, and the patched
engine source with a rebuild script. Credits makes the source bundle available.

Inside the app JAR, private dylibs have a `.bin` resource suffix so Compose's
automatic native-library signing cannot silently invalidate their hashes.
Extraction restores their real names. The explicit release signing tool signs
these payloads and the emulator, updates the manifest, and only then signs the enclosing
app. Both architecture-specific DMGs require notarization, stapling and final
native packaged-runtime checks before publication. The Mac TCI build explicitly
omits `pthread_jit_write_protect_np`: interpreter bytecode uses ordinary writable
memory, not native JIT code. This prevents the hardened-runtime startup crash
found during final signing QA without adding an emulator JIT entitlement.

## Local validation, October 11, 2026

Apple silicon native and packaged-app checks passed: live demo boot, 256-color
graphics, keyboard input, non-silent PCM transport, reset, clean process stop,
restart, Unicode/comma paths and read-only demo preservation. All 40 desktop
unit tests and the then-current packaging tests passed. The package integrity failure found during QA was fixed;
runtime verification remains enabled.

A disposable copy of the existing Windows 95 test image reached a clean
640 x 480 desktop through the C&T/ESS hardware configuration. ScanDisk selection,
Exit/Enter and its follow-up prompt responded to keyboard input. This establishes
a real Windows 95 boot on this Mac, not complete compatibility with every image.
On a fresh PC110-mode boot, Display Settings opened directly and reported
256 colors at 640 x 480. Applying the guest's Clouds wallpaper produced a clean
desktop frame with 78 distinct colors, establishing output beyond 16-color VGA
without replacing the guest display driver. Full applications, long sessions,
and physical Intel Mac execution remain separate validation items. Windows
startup also produced non-silent PCM through the pipe, but physical speaker
output and the complete ESS guest-driver feature set are not verified.

The native C&T black-box probe also passed using the imported BIOS: chip ID,
512 KiB VRAM reporting, the `INT 10h AX=5F10h` ABI used by CHIPS.DRV, wide writes
through both packed banks, and coherent banked/linear memory. This is device
validation, not a substitute for the Windows driver's full drawing tests.
The initial DOS dirty-shutdown prompt still shows a text-layout artifact on the
historical image; ScanDisk's own interface and the Windows desktop render cleanly.

Further guest QA found a fatal exception in VMM during a rapid four-tab sequence
in Display Properties. A fresh PC110 boot opened Settings directly without that
crash. A Cirrus-driver comparison also opened Settings and traversed the tabs
individually. The crash's cause has not been isolated, so successful desktop
operation must not be described as complete Windows 95 compatibility. This
stability issue and the text-layout artifact remain limits before claiming
stable Windows compatibility, alongside broader guest-driver and Intel Windows
execution checks. The generic-adapter comparison
is a diagnostic script option, not a new machine-profile control in the app.

The PC110-mode guest and both generic-adapter comparison guests completed
Start-menu shutdown and cleared the FAT dirty flag in their disposable disk
copies. Source media was never
attached writable or modified. Hardware Power off remains distinct from guest
shutdown and can cause another ScanDisk request.

Private disks and captures remain local and are excluded from CI/release assets.
The early local app used a QA-only JDK packaging override and was not a signed
or notarized installer. The separate [1.0.2 release validation record](QA-MACOS-1.0.2.md)
covers release-JDK builds and final signed-installer checks on both architectures.
