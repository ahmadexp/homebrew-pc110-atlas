# Bundled Java runtime

Desktop 1.0.0 uses Eclipse Temurin 21.0.12.1+1-LTS. The setup-java version
notation is `21.0.12+101.0`, where `101` encodes patch 1 and build 1.
Snap uses the same pinned Linux JDK and verifies its download checksum.

The public release includes these corresponding source and build inputs:

- `OpenJDK21U-jdk-sources_21.0.12.1_1.tar.gz`: complete Temurin OpenJDK source.
- The matching `.tar.gz.json`: upstream build configuration and provenance.
- `temurin-build-e6ba7dec3d07654074559310376a3ae89da5f4ac.tar.gz`: the build
  scripts identified by the upstream metadata.

The JRE is a jlink subset of that runtime. No changes to the runtime source
are made by PC110 Atlas. Preserve its bundled `legal` directory. The Java
runtime retains GPLv2 with the Classpath Exception and component notices;
the original PC110 Atlas code remains MIT licensed. See
[Adoptium's license information](https://adoptium.net/docs/faq) and
[OpenJDK's license](https://openjdk.org/legal/gplv2+ce.html).

`download-runtime-sources.py` retrieves and verifies the release source
attachments. When updating Java, update `java-version.txt`, `java-runtime.json`,
`runtime-source-files.json`, and this document together, then rebuild the
installers and snaps.
