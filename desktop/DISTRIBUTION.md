# Desktop distribution

The packaging targets are Snap Store (Ubuntu App Center), APT, YUM/DNF,
Chocolatey, and Homebrew. The workflows prepare real installers and derive
checksums from their contents. Version 1.0.0 has public Linux and Windows
installers, tested Snap and Chocolatey packages, and an experimental IRIX source
kit. [Snap Store](https://snapcraft.io/pc110-atlas), APT and YUM/DNF are live.
Chocolatey Community submission and the notarized Homebrew release are still pending.

The shared desktop edition uses the portable PC110 core on Linux, Windows, and
macOS. The Homebrew edition is separate from the SwiftUI Mac Catalyst app and
its QEMU backend. IRIX uses the smaller [C/X11 Unix edition](../unix/README.md).

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
./android/gradlew -p desktop test packageDmg

# Release tooling tests
python3 -m unittest discover -s desktop/packaging/tests -v
```

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
Mac notarization remains pending.

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

Create a Chocolatey Community account and obtain its publishing API key. Run
`bash desktop/packaging/configure-chocolatey.sh` in an interactive terminal to
save the key directly to the public repository's `CHOCO_API_KEY` Actions secret.
The prompt hides the key, and the script does not write a plaintext key file.
Then select Chocolatey in the publish workflow. Submission enters Chocolatey's review
process and does not guarantee immediate public availability.

Version 1.0.0's public NUPKG has passed installation, launcher, and uninstall
checks on Windows using the public MSI download. The Community submission
still requires the publisher's API key.

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

After the notarized release and tap have been published:

```sh
brew tap ahmadexp/pc110-atlas
brew install --cask pc110-atlas
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

The signing script uses the same JVM entitlements as Compose, verifies the
app signature, and signs the DMG. Notarization requires an existing notarytool
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
