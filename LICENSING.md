# PC110 Atlas licensing

The original application code authored by Ahmad Byagowi is licensed under
the [MIT License](LICENSE). This declaration does not relicense third-party
code, hardware designs, artwork, documentation, trademarks, or user media.
Existing copyright and license notices continue to apply to those materials.

The Open-Source-PC110 hardware project, including its board and schematic
material, retains its CC BY-NC 4.0 terms and the creator's separate commercial
licensing rights. See the [hardware project](https://github.com/ahmadexp/Open-Source-PC110).

The portable desktop edition bundles Kotlin, Compose, Skiko/Skia, and a Java
runtime. Their upstream licenses remain in effect. Preserve the notices
inside the bundled JARs and the Java runtime's `legal` directory when
redistributing an installer. The Java runtime is OpenJDK from Eclipse Temurin,
under GPLv2 with the Classpath Exception and additional component notices.
Source releases are available from [Eclipse Adoptium](https://adoptium.net/temurin/releases/).

QEMU, SeaBIOS, GLib, and Pixman are separate third-party components used by
other application editions. Their existing license texts and corresponding
source requirements apply whenever those components are distributed. The
portable desktop release and the IRIX C/X11 source kit do not bundle QEMU or
IBM firmware. The IRIX frontend links to the workstation's system X11 library.

IBM firmware, PersonaWare, DOS, and Windows are not covered by the MIT license
and are not included in the portable desktop release or IRIX testing kit.
IBM and its product names remain their owners' trademarks. This project is
independent of IBM.
