# Desktop distribution

The packaging targets are Snap Store (Ubuntu App Center), APT, YUM/DNF,
Chocolatey, and Homebrew. The workflows prepare real installers and derive
checksums from their contents. Version 1.0.0 has public Linux and Windows
installers, notarized Mac DMGs for Intel and Apple silicon, tested Snap and Chocolatey packages, and an experimental IRIX source
kit. [Snap Store](https://snapcraft.io/pc110-atlas), APT and YUM/DNF are live.
Chocolatey Community version 1.0.0 was approved on September 23, 2026 after the
requested copyright metadata correction. Its public status was checked on
October 16, 2026.
Mac/Homebrew 1.0.3 replaces the standalone Intel and Apple silicon DMGs,
adding direct pointing and the corrected Up key.
See [release notes](RELEASE-MACOS-1.0.3.md) and [installer validation](QA-MACOS-1.0.3.md).

Windows 1.0.3 MSI/EXE and a locally tested Chocolatey package were also built
without hosted runners and published on October 17. See
[Windows release notes](RELEASE-WINDOWS-1.0.3.md) and
[native installer/package validation](QA-WINDOWS-1.0.3.md).
Chocolatey 1.0.3 was submitted on October 17 and is awaiting automated checks
and moderation. The Community Repository's approved version remains 1.0.0
until the new package is approved.

Published 1.0.0 desktop installers use the portable PC110 core. Mac 1.0.2 bundles
the native emulator, retained in Mac and Windows 1.0.3; Linux channels update separately. The Homebrew
edition remains separate from the SwiftUI Mac Catalyst app. IRIX uses the smaller
[C/X11 Unix edition](../unix/README.md).

Pi-Apps preparation is documented in [the candidate guide](packaging/pi-apps/README.md).
The ARM64 Trixie/Noble candidate has local container verification and partial
[Pi 5 testing](packaging/pi-apps/HARDWARE-TEST.md), but is not submitted or
accepted. Native picker/layout fixes, remaining hardware checks, and upstream's
supported-system requirements remain release gates. This does not add the app
to Raspberry Pi OS's official APT repositories.

## Build targets

| Channel | Package | Architecture |
| --- | --- | --- |
| Ubuntu App Center / Snap Store | Strictly confined snap | amd64, arm64 |
| APT | DEB plus signed repository | amd64, arm64 |
| YUM / DNF | RPM plus signed repository | x86_64, aarch64 |
| Chocolatey | NUPKG that installs a checksum-pinned MSI | x64 |
| Homebrew | Cask selecting a signed, notarized DMG | Intel, Apple silicon |
| IRIX 6.5 | C99/X11 source archive and native make install | MIPS n32 target |

Native Linux installers are built on Ubuntu 24.04. Other distributions must
satisfy the actual package dependencies; this does not promise support for old
CentOS or RHEL releases. A YUM/DNF repository is independent of Fedora's or
Red Hat's official repositories. APT packages are also published through this
project's own repository, rather than Ubuntu's main archive.

## Build and release

Use the Eclipse Temurin version pinned in `packaging/java-version.txt`, plus CMake 3.22 or newer.
The Compose packaging plugin rejects Homebrew's JDK for macOS packaging.
The user does not need Java installed because the runtime is bundled.

`desktop/packaging/version.txt` is the desktop release version. It is independent
of the Apple and Android store versions. Use a stable three-part version, with
MSI limits of 255.255.65535, and increase it for every public release.

```sh
# Linux
./android/gradlew -p desktop test packageDeb packageRpm

# macOS
python3 desktop/qemu/build-macos.py desktop/build/qemu-macos
python3 desktop/qemu/package-macos.py desktop/build/qemu-macos desktop/build/qemu-runtime-macos-arm64
./android/gradlew -p desktop test packageDmg -PrequireMacQemu=true

# Release tooling tests
python3 -m unittest discover -s desktop/packaging/tests -v
```

Use `qemu-runtime-macos-x64` for an Intel build. See the Mac guide for native
dependency tools and the final-signing integrity checks.

```powershell
# Windows, with WiX Toolset 3.14.1 on PATH
android\gradlew.bat -p desktop test packageMsi packageExe
```

The **Desktop packages** workflow builds five native targets and two snaps.
Its manual inputs can select a native platform and independently enable Snap builds.
Ordinary workflow builds produce unsigned macOS packages for testing. Its
installed-launcher smoke tests load the bundled native core, decode a bundled
image, and import disposable test media. Run GUI checks before promotion:
launch, import a BIOS and disk, boot, exercise keyboard and pointer input,
open a schematic, quit, upgrade, and confirm imported media remains available.
For snaps, also test removable media and the desktop portal on Ubuntu.

### Local builds without hosted runners

As of October 16, 2026, Actions is disabled for the private source repository
and its five registered build workflows are disabled. Builds and validation
run locally; source pushes and manual release uploads do not require Actions.
Do not enable a hosted workflow as a fallback without maintainer approval.
Existing workflow files remain as reference recipes, not the active release
path. Re-enabling Actions is reversible and is not needed for local builds.

GitHub-hosted jobs are optional. Run the same build, package and validation
commands from a source checkout on the appropriate local machine, then upload
only verified release assets. This does not require registering a persistent
self-hosted runner or changing GitHub billing settings. Source pushes, release
uploads and package-feed updates remain separate from build execution.

- Apple silicon Mac: build the native runtime, run the keyboard parity check
  (`python3 desktop/packaging/check-keyboard-parity.py`), run the desktop and
  packaging tests, and create the DMG using the commands above. Use a native
  CMake and the pinned Temurin JDK on `PATH`; an old Gradle daemon can retain
  another toolchain, so use `--no-daemon` when switching build environments.
- Intel Mac: run the same steps on an Intel build environment, selecting
  `qemu-runtime-macos-x64`. Keep architecture-specific output directories
  separate. An Apple silicon test does not validate the Intel installer.
  Keep the build Mac fully awake on AC power and bind `caffeinate -is` to the
  build command. Use a persistent build log so an SSH disconnect does not
  lose the build result. A successful SSH connection during a brief network
  maintenance wake is not proof that the machine will stay available.
  Build-only Python tools can use a project-specific virtual environment;
  the October 17 Intel build uses Python 3.15.0 and Meson 1.11.1 without
  changing the system Python.
- Windows x64: reproduce the WiX 3 and MSYS2 UCRT64 dependencies in the
  **Desktop packages** workflow. Run `bash desktop/qemu/build-windows.sh` from
  UCRT64, then the dependency-source collection and pipe test from that
  workflow. Build with `android\gradlew.bat -p desktop test packageMsi packageExe
  -PrequireWindowsQemu=true --no-daemon`. Test MSI installation, the installed
  launcher, guest input and display, and Chocolatey installation/uninstallation
  on Windows before promotion.

The [packaging tool requires the target operating system](https://docs.oracle.com/en/java/javase/21/jpackage/packaging-overview.html).
A Mac-only build cannot stand in for a Windows package and installation test.
The existing Mac scripts support local signing without exporting the private
key: `sign-macos-candidate.sh`, `notarize-macos.sh` and
`verify-macos-candidate.sh`. Supply the existing Developer ID and Keychain
notarization profile through their documented environment variables. Keep
credentials, personal media and the private source checkout out of release
uploads. Both Mac architectures still require signed-installer verification
before the default Homebrew cask is updated.

Configure macOS signing secrets before creating a release:

| Secret | Value |
| --- | --- |
| `MAC_CERTIFICATE_P12_BASE64` | Base64 Developer ID Application certificate and private key |
| `MAC_CERTIFICATE_PASSWORD` | Password for that P12 |
| `MAC_SIGN_ID` | Certificate identity recognized by Compose, such as the name and team ID |
| `APPLE_ID` | Apple account for notarization |
| `APPLE_APP_PASSWORD` | App-specific notarization password |
| `APPLE_TEAM_ID` | Developer team ID |

The **Desktop release** workflow is triggered by a `desktop-vVERSION` tag
matching the version file, for example `desktop-v1.0.0`. It builds and tests the
packages, signs and notarizes both DMGs, then creates a GitHub Release in the workflow's repository
with the installers, snaps, cask, Chocolatey package, Unix source archive,
and `SHA256SUMS`. A signing or build failure prevents the release. Do not
overwrite published installers: release a new version so pinned checksums
remain valid.

This application's build repository is private. Its release does not become
public automatically. Transfer validated assets to the public distribution
repository using the process below. The first public release was assembled
from successful platform builds, allowing Linux and Windows publication while
Mac notarization was pending. Mac packages were added after signing nested
native libraries and rebuilding the PC110 JNI core for macOS 12.0.

After the release exists, run **Publish desktop package channels**, enter the
version, and select the channels to publish. Snap defaults to `edge` so the
initial submission can be tested before promotion to `stable`.

## Ubuntu App Center and Snap Store

The project uses Canonical's strictly confined Snap Store path. See
[Canonical's publication guide](https://ubuntu.com/docs/snapcraft/9/how-to/publishing/publish-a-snap/)
and the [GNOME extension](https://ubuntu.com/docs/snapcraft/9/reference/extensions/gnome-extension/).

1. Sign in to Snapcraft with the publishing Ubuntu One account. The name
   `pc110-atlas` is registered to `ahmadexp` and the publishing agreement has
   been accepted. The listing editor becomes available after the first revision
   is uploaded.
2. Maintain the store listing using [the published listing record](../snap/STORE_LISTING.md).
   The initial listing includes its icon and all four Ubuntu screenshots.
3. Export a credential restricted to this snap and the channels you intend to
   publish: `snapcraft export-login --snaps=pc110-atlas snap-login.txt`.
   Store its contents as the repository secret `SNAPCRAFT_STORE_CREDENTIALS`.
   Keep that file outside this repository. The configured credential is restricted
   to `pc110-atlas`, package access/upload/release, and the four standard channels;
   it expires September 14, 2027. It uses Candid authentication, so the publishing
   repository variable `SNAPCRAFT_STORE_AUTH` is set to `candid`. The workflow
   passes credentials through environment variables instead of the removed
   `snapcraft login --with` mechanism. If rotating to Ubuntu One credentials,
   clear the Candid variable at the same time.
4. Run the publish workflow with Snap selected and channel `edge`. After the
   store accepts the upload, test installation and promote to `stable`.

For a local Ubuntu build, install Snapcraft, configure its LXD build provider,
and run `snapcraft pack` at the repository root. Local test installation:

```sh
sudo snap install --dangerous ./pc110-atlas_1.0.0_amd64.snap
sudo snap connect pc110-atlas:removable-media
snap run pc110-atlas
```

Once published to stable:

```sh
sudo snap install pc110-atlas
```

The snap has desktop, home, audio playback, network, and optional removable-media
interfaces. `network` supports opening project links; the emulator does not
upload imported media. Removable-media access requires the explicit connection
above. Media lives under `$SNAP_USER_COMMON/pc110-atlas`, preserving it across
snap refreshes. Hidden files outside the snap's private directory are subject
to snap confinement.

## APT and YUM/DNF

The publisher produces a complete static repository with signed APT `InRelease`
and `Release.gpg`, signed RPM packages, and signed RPM `repomd.xml` metadata.
The generated `.repo` enables both `gpgcheck` and `repo_gpgcheck`.

A dedicated RSA signing key is configured for the public distribution repository.
Its fingerprint is `4B6FA5B0B9C8CC49F0C164C66D199F8D554224BC`. Keep an offline
backup of the primary key and its revocation certificate. Put its ASCII-armored signing-subkey export in `LINUX_GPG_PRIVATE_KEY` and
its full public fingerprint in the repository variable `LINUX_GPG_KEY_ID`.
The unattended workflow uses the exported signing subkey without an interactive
passphrase. The primary certification key stays in the local backup and is not
provided to GitHub Actions. Publish the fingerprint alongside your install
instructions so users can verify the key.

Enable GitHub Pages with **GitHub Actions** as the deployment source for this
repository. The Linux publisher deploys the entire Pages site as a package
repository. If Pages already serves another website, use a separate hosting
repository or run the generator and upload its output to another HTTPS host.

Manual generation on Ubuntu:

```sh
sudo apt install apt-utils rpm createrepo-c gnupg
python3 desktop/packaging/build-repositories.py \
  --assets desktop/build/release --output desktop/build/repository \
  --base-url https://ahmadexp.github.io/homebrew-pc110-atlas \
  --key YOUR_FULL_SIGNING_KEY_FINGERPRINT
```

Generation requires an empty output directory. Each deployment contains the
selected release; earlier installers remain on GitHub Releases. Clients with
old cached metadata may need `apt update` or `dnf clean metadata` after a release.
The generator can also include several releases in its input to retain older
versions in the package repository. Minimal headless test containers may need
`sudo install -d /usr/share/desktop-directories` before installing the GUI
package, since they do not include a desktop environment.

The repository is live at the URL below:

```sh
# Ubuntu / Debian
curl -fsSLo pc110-atlas.asc https://ahmadexp.github.io/homebrew-pc110-atlas/keys/pc110-atlas.asc
gpg --show-keys --fingerprint pc110-atlas.asc
# Compare the fingerprint with the maintainer's published fingerprint.
gpg --dearmor --output pc110-atlas.gpg pc110-atlas.asc
sudo install -m 644 pc110-atlas.gpg /usr/share/keyrings/pc110-atlas.gpg
echo 'deb [signed-by=/usr/share/keyrings/pc110-atlas.gpg] https://ahmadexp.github.io/homebrew-pc110-atlas/apt stable main' | sudo tee /etc/apt/sources.list.d/pc110-atlas.list
sudo apt update
sudo apt install pc110-atlas
```

```sh
# Fedora / compatible RPM-based systems
curl -fsSLo pc110-atlas.repo https://ahmadexp.github.io/homebrew-pc110-atlas/pc110-atlas.repo
sudo install -m 644 pc110-atlas.repo /etc/yum.repos.d/pc110-atlas.repo
sudo dnf install pc110-atlas
# Or, on a compatible system providing yum:
sudo yum install pc110-atlas
```

Check the displayed signing-key fingerprint on first installation. No global
APT trusted-key entry or disabled signature check is needed. For a direct
local install, `sudo apt install ./file.deb` or
`sudo dnf install ./file.rpm` installs a downloaded native package.

## Chocolatey

The generated package downloads the x64 MSI from the exact desktop release,
checks SHA-256, and installs it silently. MSI registration enables Chocolatey's
automatic uninstall. This follows the
[Chocolatey MSI packaging guide](https://docs.chocolatey.org/en-us/guides/create/create-msi-package/).

For the local-only 1.0.3 release, build and test the NUPKG on Windows, including
installation from the public checksum-pinned MSI and automatic removal. Submit
with `choco push pc110-atlas.1.0.3.nupkg --source https://push.chocolatey.org/`
using the maintainer's publishing credential through a secure local prompt or
existing Chocolatey configuration. Do not put the key in source files or logs.
The website no longer supports direct NUPKG uploads. Submission enters a
separate review process and does not guarantee immediate approval.

The historical hosted publishing workflow remains documented below, but is
not used for this release and must not be dispatched without authorization.
Create a Chocolatey Community account and obtain its publishing API key. Run
`bash desktop/packaging/configure-chocolatey.sh` in an interactive terminal to
save the key directly to the public repository's `CHOCO_API_KEY` Actions secret.
The prompt hides the key, and the script does not write a plaintext key file.
Then select Chocolatey in the publish workflow. Submission enters Chocolatey's review
process and does not guarantee immediate public availability.

Package icons use jsDelivr, pinned to the matching `desktop-vVERSION` GitHub tag.
That tag must contain `desktop/packaging/pc110-atlas.png`; do not use a GitHub
raw URL or a moving branch for the Chocolatey `iconUrl`.

Package metadata must include `<copyright>Copyright (c) 2026 Ahmad Byagowi</copyright>`,
matching the upstream `LICENSE`. A manifest regression test checks both presence
and the exact license text before a package is built.

For a moderation correction to an unapproved package, run **Prepare and test
Chocolatey package** with the same version and `replace_package` enabled.
It tests installation, launch, and uninstall before replacing only the NUPKG
and its checksum entry. Other release assets and checksums are preserved.
Then run **Publish desktop package channels** with only Chocolatey selected,
and respond in the package page's **Add to Review Comments** box.
Do not replace a package version that Chocolatey has already approved.

Version 1.0.0's corrected public NUPKG passed installation, launcher, and uninstall
checks on Windows using the unchanged public MSI download in the
[September 15 package build](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/34980697863).
The original submission passed Chocolatey's validation, verification, and virus
scanning. A moderator requested a CDN-hosted icon; the corrected package uses
jsDelivr pinned to the existing `desktop-v1.0.0` tag. The same version was
[resubmitted successfully](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/34980975480)
on September 15, 2026, and the maintainer response was posted to the
[package review](https://community.chocolatey.org/packages/pc110-atlas/1.0.0).
On September 21 the moderator confirmed the MSI version and checksum, and
requested the missing copyright field. The same 1.0.0 package was rebuilt with
`Copyright (c) 2026 Ahmad Byagowi`, matching the upstream license. This was the
only metadata change; the installer script is byte-for-byte unchanged and all
other release asset checksums are preserved. Ten release tests and Windows
installation, launcher, and uninstall checks passed in
[the corrected package build](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/35626059075).
The [resubmission succeeded](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/35626294955).
The package was approved on September 23, 2026 and is publicly installable,
as verified on October 16, 2026.
Chocolatey's package download CDN may retain the old NUPKG for 30 minutes after
resubmission. No installer or other distribution channel was republished.

Before submission, test the downloaded package from its directory:

```powershell
choco install pc110-atlas --source . --version 1.0.0 -y
choco uninstall pc110-atlas -y
```

After approval: `choco install pc110-atlas`. The existing user media directory
is preserved by ordinary MSI uninstall.

## Homebrew

The public distribution repository is `ahmadexp/homebrew-pc110-atlas`.
Its publish workflow updates its own `Casks/pc110-atlas.rb` using the scoped
workflow token. No separate Homebrew account or token is required for this
configuration. An optional external tap can use `HOMEBREW_TAP_REPOSITORY` and
`HOMEBREW_TAP_TOKEN` instead.

Install the notarized release from the project's tap:

```sh
brew tap ahmadexp/pc110-atlas
brew trust --cask ahmadexp/pc110-atlas/pc110-atlas
brew install --cask pc110-atlas
```

Homebrew 6 and later require trust for third-party packages. The command above
trusts only the PC110 Atlas cask, not the entire tap. Only grant trust if you
trust this project's package code to run with your user privileges. See
[Homebrew's tap trust documentation](https://docs.brew.sh/Tap-Trust).

Alternatively, install using the fully qualified cask name. This works on older
Homebrew versions without the `trust` command and grants cask-only trust on
Homebrew 6 and later:

```sh
brew install --cask ahmadexp/pc110-atlas/pc110-atlas
```

To update an existing installation:

```sh
brew upgrade --cask pc110-atlas
```

The tap gives a working installation channel without waiting for inclusion in
Homebrew's central cask repository. Normal uninstall preserves media;
`brew uninstall --cask --zap pc110-atlas` also deletes this desktop edition's
`~/Library/Application Support/PC110 Atlas` directory and imported media.

## Distribution terms

The owner has selected MIT for the original application code. See
[LICENSE](../LICENSE) and [LICENSING.md](../LICENSING.md) for its scope.
Hardware material retains its CC BY-NC 4.0 terms, and bundled libraries retain
their own licenses. Snap and RPM metadata identify the application and
hardware terms as `MIT AND CC-BY-NC-4.0`.

## Public distribution repository

The application development repository is private. Do not use its URLs for
public installer downloads. Export only the intended public distribution files:

```sh
python3 desktop/packaging/export-public-distribution.py --output build/public-distribution
```

The public repository `ahmadexp/homebrew-pc110-atlas` hosts the versioned
installers, IRIX source kit, package publishing workflow, and Homebrew cask.
Run channel publishing in that repository. Configure its Pages source as
GitHub Actions. Its workflow token handles same-repository releases, Pages,
and cask updates; no broad personal access token is needed.

The private build workflow produces candidate artifacts. Download candidates
from a successful, identified commit, complete signing/notarization, and
render manifests with `--repository ahmadexp/homebrew-pc110-atlas` before
uploading public assets. `--channel chocolatey` or `--channel homebrew` renders
one channel independently. A channel can be published after its own required
artifacts pass validation, without waiting for unrelated publisher accounts.

The Snap Store requires an Ubuntu One publisher account, snap-name
registration, and its publishing agreement. The Chocolatey Community
Repository requires a publisher account and an API key. Put credentials
in GitHub Actions secrets, never in issue comments, release files, or Git.

## Local macOS signing and notarization

For the first notarization login, sign in to [Apple Account](https://account.apple.com/)
and generate an app-specific password in Sign-In and Security. Run
`bash desktop/packaging/configure-notarization.sh` in an interactive macOS terminal.
It asks for the Apple Account email for team `TWFK4FAG36`, then lets Apple's
`notarytool` prompt privately for the app-specific password. It validates and
stores the credentials in local Keychain profile `pc110-atlas-publishing`.
Do not paste this password into chat or commit it to Git.

CI candidates can be signed with the existing local Developer ID without
exporting its private key:

```sh
export JAVA_HOME=/path/to/temurin-21/Contents/Home
export MAC_SIGN_ID='Ahmad Byagowi (TWFK4FAG36)'
bash desktop/packaging/sign-macos-candidate.sh candidate.dmg signed-output.dmg
NOTARY_KEYCHAIN_PROFILE=your-profile bash desktop/packaging/notarize-macos.sh signed-output.dmg
```

The signing script first signs the native payloads inside packaged JARs,
including `.dylib`, `.jnilib`, Mac emulator executables and private `.dylib.bin`
resources. It refreshes matching `.sha256` cache keys and the runtime's integrity
manifest, preserves unrelated
archive contents, and refuses to invalidate existing Java archive signatures.
It then uses the same JVM entitlements as Compose, verifies the app signature,
and signs the DMG. Checking only the outer app with `codesign --deep` does not
validate native code inside JAR archives. Test the final packaged launcher
again after signing. Regression tests cover archive preservation, checksum
refresh and failed signing without replacing the original JAR.

After notarization and stapling, run the final checks on each native architecture:

```sh
bash desktop/packaging/verify-macos-candidate.sh signed-output.dmg new-evidence-directory 1.0.2
```

This checks Gatekeeper, signatures, version and architecture, then boots the
bundled demo and tests graphics, input, PCM transport, reset and restart. It does
not substitute for private operating-system or full guest-driver validation.

The PC110 native CMake target defaults to macOS 12.0 before compiler detection.
For old candidates built with the build host's newer deployment target, rebuild
the JNI library from the same source revision with
`-DCMAKE_OSX_DEPLOYMENT_TARGET=12.0` and the matching
`-DCMAKE_OSX_ARCHITECTURES=x86_64` or `arm64`. Pass the resulting library to the
signing script through `PC110_NATIVE_LIBRARY=/absolute/path/libpc110_desktop.dylib`.
The script checks its architecture against the packaged launcher before
replacing the single PC110 JNI resource and signing it. Confirm the minimum
version with `xcrun vtool -show-build`, record the rebuild in release provenance,
and rerun the package smoke test. Do not relabel a macOS 15 binary as macOS 12.

Notarization requires an existing notarytool
Keychain profile or the Apple account secrets listed above. Regenerate cask
checksums after notarization and stapling, which change the DMG bytes.

## Runtime source attachments

Both Snap and native installers use Eclipse Temurin 21.0.12.1+1-LTS. Preserve
its runtime notices and attach the matching sources to every public release:

```sh
python3 desktop/packaging/download-runtime-sources.py --output desktop/build/release
```

See [runtime source details](packaging/RUNTIME-SOURCES.md). These attachments
and the build metadata accompany the installers in the public release.
