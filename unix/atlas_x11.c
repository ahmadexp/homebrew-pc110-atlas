/* PC110 Atlas: a small C99/Xlib host for IRIX 6.5 and other X11 Unix systems. */
#define _POSIX_C_SOURCE 200112L
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/keysym.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/select.h>
#include <unistd.h>
#include "PC110Core/PC110Core.h"
#include "pixel.h"

enum { WIDTH = 640, HEIGHT = 560, DISPLAY_Y = 48, FRAME_HEIGHT = 480 };
static const char *tabs[] = { "Discover", "Emulator", "Hardware", "Archive", "Help" };
static Display *display;
static Window window;
static GC gc;
static XImage *image;
static Visual *visual;
static unsigned long palette[216], white, black;
static int indexed, tab, paused, running = 1, powered, test_frame;
static PC110Machine *machine;

static double seconds(void) {
    struct timeval now;
    gettimeofday(&now, NULL);
    return (double)now.tv_sec + (double)now.tv_usec / 1000000.0;
}

static unsigned long pixel(uint32_t argb) {
    if (indexed) {
        unsigned int r = (((argb >> 16) & 255U) * 5U + 127U) / 255U;
        unsigned int g = (((argb >> 8) & 255U) * 5U + 127U) / 255U;
        unsigned int b = ((argb & 255U) * 5U + 127U) / 255U;
        return palette[r * 36U + g * 6U + b];
    }
    return atlas_pixel(argb, visual->red_mask, visual->green_mask, visual->blue_mask);
}

static void text(int x, int y, const char *value) {
    XDrawString(display, window, gc, x, y, value, (int)strlen(value));
}

static void page(const char *const *lines) {
    int i;
    for (i = 0; lines[i]; ++i) text(20, 90 + i * 25, lines[i]);
}

static void draw(void) {
    int i, x, y;
    static const char *discover[] = {
        "PC110 Atlas for Unix", "An interactive companion to the IBM Palm Top PC 110.", "",
        "This lightweight edition uses the portable PC110 emulator.",
        "Choose Emulator to view the guest, or browse the reference tabs.", "",
        "Start with your own BIOS and raw disk image:",
        "pc110-atlas-unix --bios PC110.rom --disk HDD.img", "",
        "No IBM firmware or operating-system media is bundled.",
        "Project: github.com/ahmadexp/PC110-Atlas", NULL
    };
    static const char *hardware[] = {
        "PC110 hardware reference", "",
        "Mainboard: 10 copper layers; 6,088 physical vias.",
        "PSU: 4 layers. Modem: 6 layers. RAM: 4 layers. Dock: 4 layers.",
        "The emulator presents a 640 x 480 guest framebuffer.", "",
        "Schematics and board sources:", "github.com/ahmadexp/Open-Source-PC110/tree/main/PCB", "",
        "Use the full desktop edition for interactive PCB layer stacks.", NULL
    };
    static const char *archive[] = {
        "PC110 archive and credits", "",
        "Explore the portable computer's history in the project archive:",
        "github.com/ahmadexp/PC110-Atlas", "",
        "Portable emulator source: github.com/ahmadexp/PC110-EMU", "",
        "IBM, PC DOS, and PersonaWare belong to their respective owners.",
        "This project is independent of IBM.",
        "Hardware material retains its original licensing terms.", NULL
    };
    static const char *help[] = {
        "Controls", "",
        "Click a tab to switch pages.",
        "Ctrl+Shift+P: pause or resume. Ctrl+Shift+R: reset.",
        "Ctrl+Shift+Q: quit. Window close also quits.",
        "Guest keys: letters, numbers, function and navigation keys.",
        "Guest pointer: move and click inside the emulator display.", "",
        "Disk changes stay in memory and are discarded when you exit.",
        "IRIX target: 6.5, MIPS n32, GCC C99, system X11.",
        "Guest audio, 3D boards, and embedded PDF viewing are unavailable.", NULL
    };
    XSetForeground(display, gc, black);
    XFillRectangle(display, window, gc, 0, 0, WIDTH, HEIGHT);
    XSetForeground(display, gc, white);
    for (i = 0; i < 5; ++i) {
        if (i == tab) XDrawRectangle(display, window, gc, i * 128 + 2, 4, 123, 30);
        text(i * 128 + 18, 24, tabs[i]);
    }
    if (tab == 1 && (powered || test_frame)) {
        const uint32_t *frame = pc110_get_framebuffer(machine);
        if (frame) {
            for (y = 0; y < FRAME_HEIGHT; ++y)
                for (x = 0; x < WIDTH; ++x)
                    XPutPixel(image, x, y, pixel(test_frame ? (x < 213 ? 0xffff0000U : x < 426 ? 0xff00ff00U : 0xff0000ffU) : frame[y * WIDTH + x]));
            XPutImage(display, window, gc, image, 0, 0, 0, DISPLAY_Y, WIDTH, FRAME_HEIGHT);
        }
    } else if (tab == 1) {
        text(20, 100, "No BIOS loaded. Start with --bios /path/to/your/PC110.rom");
        text(20, 130, "Add --disk /path/to/your/raw-disk.img to attach boot media.");
    } else if (tab == 0) page(discover);
    else if (tab == 2) page(hardware);
    else if (tab == 3) page(archive);
    else page(help);
    text(12, 548, powered ? (paused ? "Paused | Ctrl+Shift+P: resume" : "Running | Ctrl+Shift+P: pause")
                           : "Reference mode | Supply your own BIOS to start the emulator");
    XFlush(display);
}

static unsigned int scan_code(KeySym key) {
    static const char *rows[] = { "1234567890-=", "qwertyuiop[]", "asdfghjkl;'`", "zxcvbnm,./" };
    static const unsigned int starts[] = { 0x02, 0x10, 0x1e, 0x2c };
    unsigned int row;
    if (key >= XK_A && key <= XK_Z) key += XK_a - XK_A;
    for (row = 0; row < 4; ++row) {
        const char *found = key > 0 && key < 128 ? strchr(rows[row], (int)key) : NULL;
        if (found) return starts[row] + (unsigned int)(found - rows[row]);
    }
    if (key >= XK_F1 && key <= XK_F10) return 0x3bU + (unsigned int)(key - XK_F1);
    switch (key) {
        case XK_Escape: return 0x01;
        case XK_BackSpace: return 0x0e;
        case XK_Tab: case XK_ISO_Left_Tab: return 0x0f;
        case XK_Return: case XK_KP_Enter: return 0x1c;
        case XK_backslash: return 0x2b;
        case XK_space: return 0x39;
        case XK_Home: case XK_KP_Home: return 0x47;
        case XK_Up: case XK_KP_Up: return 0x48;
        case XK_Prior: case XK_KP_Prior: return 0x49;
        case XK_Left: case XK_KP_Left: return 0x4b;
        case XK_Right: case XK_KP_Right: return 0x4d;
        case XK_End: case XK_KP_End: return 0x4f;
        case XK_Down: case XK_KP_Down: return 0x50;
        case XK_Next: case XK_KP_Next: return 0x51;
        case XK_Insert: case XK_KP_Insert: return 0x52;
        case XK_Delete: case XK_KP_Delete: return 0x53;
        case XK_F11: return 0x57;
        case XK_F12: return 0x58;
        default: return 0;
    }
}

static void keyboard(XKeyEvent *event, int down) {
    char buffer[16];
    KeySym translated, base = XLookupKeysym(event, 0);
    int length = XLookupString(event, buffer, sizeof(buffer), &translated, NULL);
    unsigned int state = event->state, flags = 0, scan;
    unsigned int modifier = (base == XK_Shift_L || base == XK_Shift_R) ? ShiftMask
        : (base == XK_Control_L || base == XK_Control_R) ? ControlMask
        : (base == XK_Alt_L || base == XK_Alt_R) ? Mod1Mask : 0;
    if (modifier) state = down ? state | modifier : state & ~modifier;
    if (down && (state & ControlMask) && (state & ShiftMask)) {
        if (base == XK_q || base == XK_Q) { running = 0; return; }
        if (base == XK_p || base == XK_P) { paused = !paused; return; }
        if (base == XK_r || base == XK_R) { if (powered) pc110_reset(machine); return; }
    }
    if (!powered || tab != 1) return;
    if (state & ShiftMask) flags |= 0x03;
    if (state & ControlMask) flags |= 0x04;
    if (state & Mod1Mask) flags |= 0x08;
    if (state & LockMask) flags |= 0x40;
    pc110_key_modifiers(machine, (uint16_t)flags);
    scan = scan_code(base);
    if (down && scan) {
        unsigned int ascii = length == 1 ? (unsigned char)buffer[0] : 0;
        if (base == XK_Delete || base == XK_KP_Delete) ascii = 0;
        pc110_key_bios(machine, (uint16_t)((scan << 8) | ascii));
    }
}

static int valid_file(const char *path, long maximum, int disk) {
    struct stat info;
    if (stat(path, &info) || !S_ISREG(info.st_mode) || info.st_size <= 0 || info.st_size > maximum
        || (disk && info.st_size % 512 != 0)) {
        fprintf(stderr, "Invalid %s: %s (maximum %ld bytes%s)\n", disk ? "disk" : "BIOS", path,
                maximum, disk ? ", whole 512-byte sectors required" : "");
        return 0;
    }
    return 1;
}

int main(int argc, char **argv) {
    const char *bios = NULL, *disk = NULL;
    int i, screen, depth, frames = 0, smoke_frames = 0, fps = 15, instructions = 40000;
    double next_frame;
    XVisualInfo chosen;
    XSetWindowAttributes attributes;
    XSizeHints size;
    XClassHint class_hint;
    Atom close_window;
    Colormap colormap;
    for (i = 1; i < argc; ++i) {
        if (!strcmp(argv[i], "--help")) {
            puts("Usage: pc110-atlas-unix [--bios FILE] [--disk FILE] [--fps 1..60] [--instructions 1000..1000000] [--smoke-test]");
            return 0;
        } else if (!strcmp(argv[i], "--smoke-test")) { smoke_frames = 3; test_frame = 1; tab = 1; }
        else if ((!strcmp(argv[i], "--bios") || !strcmp(argv[i], "--disk")) && i + 1 < argc) {
            if (!strcmp(argv[i], "--bios")) bios = argv[++i]; else disk = argv[++i];
        } else if ((!strcmp(argv[i], "--fps") || !strcmp(argv[i], "--instructions")) && i + 1 < argc) {
            int is_fps = !strcmp(argv[i], "--fps");
            char *end;
            long value = strtol(argv[++i], &end, 10);
            if (*end || value < (is_fps ? 1 : 1000) || value > (is_fps ? 60 : 1000000)) {
                fprintf(stderr, "Invalid timing option: %s\n", argv[i]); return 2;
            }
            if (is_fps) fps = (int)value; else instructions = (int)value;
        } else { fprintf(stderr, "Unknown or incomplete argument: %s\n", argv[i]); return 2; }
    }
    if (disk && !bios) { fputs("--disk requires --bios\n", stderr); return 2; }
    if (bios && !valid_file(bios, 1024L * 1024L, 0)) return 2;
    if (disk && !valid_file(disk, 512L * 1024L * 1024L, 1)) return 2;
    machine = pc110_create();
    if (!machine) { fputs("Not enough memory for the PC110 core\n", stderr); return 1; }
    if (bios) {
        if (!pc110_load_bios(machine, bios) || (disk && !pc110_attach_boot_image(machine, disk))) {
            fputs("Could not load personal media\n", stderr); pc110_destroy(machine); return 1;
        }
        pc110_reset(machine);
        powered = 1;
        tab = 1;
    }
    display = XOpenDisplay(NULL);
    if (!display) { fputs("Cannot open X display. Set DISPLAY to your X server.\n", stderr); pc110_destroy(machine); return 1; }
    screen = DefaultScreen(display);
    visual = DefaultVisual(display, screen);
    depth = DefaultDepth(display, screen);
    if (XMatchVisualInfo(display, screen, 24, TrueColor, &chosen)
        || XMatchVisualInfo(display, screen, 16, TrueColor, &chosen)) {
        visual = chosen.visual; depth = chosen.depth;
    }
    indexed = visual->class != TrueColor;
    if (indexed && visual->class != PseudoColor) {
        fputs("An X11 TrueColor or PseudoColor visual is required\n", stderr);
        XCloseDisplay(display); pc110_destroy(machine); return 1;
    }
    colormap = XCreateColormap(display, RootWindow(display, screen), visual, AllocNone);
    if (indexed) {
        for (i = 0; i < 216; ++i) {
            XColor color;
            color.red = (unsigned short)((i / 36) * 13107);
            color.green = (unsigned short)(((i / 6) % 6) * 13107);
            color.blue = (unsigned short)((i % 6) * 13107);
            color.flags = DoRed | DoGreen | DoBlue;
            if (!XAllocColor(display, colormap, &color)) {
                fputs("Cannot allocate an X11 color cube\n", stderr);
                XFreeColormap(display, colormap); XCloseDisplay(display); pc110_destroy(machine); return 1;
            }
            palette[i] = color.pixel;
        }
    }
    white = pixel(0xffffffffU); black = pixel(0xff000000U);
    attributes.colormap = colormap;
    attributes.background_pixel = black;
    attributes.border_pixel = black;
    attributes.event_mask = ExposureMask | KeyPressMask | KeyReleaseMask | ButtonPressMask
        | ButtonReleaseMask | PointerMotionMask | FocusChangeMask;
    window = XCreateWindow(display, RootWindow(display, screen), 0, 0, WIDTH, HEIGHT, 0, depth,
        InputOutput, visual, CWColormap | CWBackPixel | CWBorderPixel | CWEventMask, &attributes);
    XStoreName(display, window, "PC110 Atlas for Unix");
    class_hint.res_name = "pc110-atlas-unix"; class_hint.res_class = "PC110Atlas";
    XSetClassHint(display, window, &class_hint);
    memset(&size, 0, sizeof(size));
    size.flags = PMinSize | PMaxSize;
    size.min_width = size.max_width = WIDTH; size.min_height = size.max_height = HEIGHT;
    XSetWMNormalHints(display, window, &size);
    close_window = XInternAtom(display, "WM_DELETE_WINDOW", False);
    XSetWMProtocols(display, window, &close_window, 1);
    gc = XCreateGC(display, window, 0, NULL);
    image = XCreateImage(display, visual, (unsigned int)depth, ZPixmap, 0, NULL, WIDTH, FRAME_HEIGHT, 32, 0);
    if (!image || !(image->data = calloc((size_t)image->bytes_per_line, FRAME_HEIGHT))) {
        fputs("Cannot allocate X framebuffer\n", stderr);
        if (image) XDestroyImage(image);
        XFreeGC(display, gc); XDestroyWindow(display, window); XFreeColormap(display, colormap);
        XCloseDisplay(display); pc110_destroy(machine); return 1;
    }
    XMapWindow(display, window);
    next_frame = seconds();
    while (running) {
        while (XPending(display)) {
            XEvent event;
            XNextEvent(display, &event);
            if (event.type == ClientMessage && (Atom)event.xclient.data.l[0] == close_window) running = 0;
            else if (event.type == KeyPress || event.type == KeyRelease) keyboard(&event.xkey, event.type == KeyPress);
            else if (event.type == FocusOut) {
                pc110_key_modifiers(machine, 0);
                for (i = 0; i < 3; ++i) pc110_mouse_up(machine, 0, 0, i);
            } else if (event.type == ButtonPress && event.xbutton.y < 40) {
                if (event.xbutton.x >= 0 && event.xbutton.x < WIDTH) {
                    tab = event.xbutton.x / 128;
                    pc110_key_modifiers(machine, 0);
                    for (i = 0; i < 3; ++i) pc110_mouse_up(machine, 0, 0, i);
                }
            } else if (powered && tab == 1 && (event.type == MotionNotify || event.type == ButtonPress || event.type == ButtonRelease)) {
                int x = event.type == MotionNotify ? event.xmotion.x : event.xbutton.x;
                int y = (event.type == MotionNotify ? event.xmotion.y : event.xbutton.y) - DISPLAY_Y;
                if ((x >= 0 && x < WIDTH && y >= 0 && y < FRAME_HEIGHT) || event.type == ButtonRelease) {
                    if (x < 0) x = 0;
                    if (x >= WIDTH) x = WIDTH - 1;
                    if (y < 0) y = 0;
                    if (y >= FRAME_HEIGHT) y = FRAME_HEIGHT - 1;
                    if (event.type == MotionNotify) pc110_mouse_move(machine, x, y);
                    else if (event.xbutton.button <= 3) {
                        int button = event.xbutton.button == 1 ? 0 : event.xbutton.button == 3 ? 1 : 2;
                        if (event.type == ButtonPress) pc110_mouse_down(machine, x, y, button);
                        else pc110_mouse_up(machine, x, y, button);
                    }
                }
            }
            draw();
        }
        if (seconds() >= next_frame) {
            if (powered && !paused) {
                pc110_cpu_set_trace_mode(machine, 0);
                pc110_cpu_step(machine, instructions);
                pc110_run_frame(machine);
            }
            draw();
            if (smoke_frames && ++frames >= smoke_frames) running = 0;
            next_frame = seconds() + 1.0 / fps;
        }
        if (running) {
            fd_set readers;
            struct timeval delay;
            double remaining = next_frame - seconds();
            int result;
            if (remaining < 0 || remaining > 1) remaining = 0;
            delay.tv_sec = 0; delay.tv_usec = (long)(remaining * 1000000);
            FD_ZERO(&readers); FD_SET(ConnectionNumber(display), &readers);
            result = select(ConnectionNumber(display) + 1, &readers, NULL, NULL, &delay);
            if (result < 0 && errno != EINTR) { perror("select"); running = 0; }
        }
    }
    XDestroyImage(image); XFreeGC(display, gc); XDestroyWindow(display, window);
    XFreeColormap(display, colormap); XCloseDisplay(display); pc110_destroy(machine);
    if (smoke_frames) puts("PC110 Atlas X11 smoke test passed");
    return 0;
}
