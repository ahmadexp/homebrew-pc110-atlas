#define _XOPEN_SOURCE 600
#define _POSIX_C_SOURCE 200112L
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "PC110Core/PC110Core.h"
#include "../pixel.h"

int main(void) {
    PC110Machine *machine = pc110_create();
    unsigned char bios[65536];
    /* Original test ROM: write 0xbeef at guest address 0x600, then halt. */
    const unsigned char code[] = {0xb8, 0, 0, 0x8e, 0xd8, 0xc7, 0x06, 0, 0x06, 0xef, 0xbe, 0xf4, 0xeb, 0xfd};
    const unsigned char reset[] = {0xea, 0, 0, 0, 0xf0};
    char path[] = "/tmp/pc110-unix-bios-XXXXXX";
    int fd = mkstemp(path);
    FILE *stream;
    assert(machine && fd >= 0);
    stream = fdopen(fd, "wb");
    assert(stream);
    memset(bios, 0xff, sizeof(bios));
    memcpy(bios, code, sizeof(code));
    memcpy(bios + 0xfff0, reset, sizeof(reset));
    assert(fwrite(bios, 1, sizeof(bios), stream) == sizeof(bios));
    assert(fclose(stream) == 0);
    assert(pc110_load_bios(machine, path));
    assert(unlink(path) == 0);
    pc110_reset(machine);
    pc110_cpu_step(machine, 1000);
    assert(pc110_mem_read8(machine, 0x600) == 0xef);
    assert(pc110_mem_read8(machine, 0x601) == 0xbe);
    pc110_run_frame(machine);
    assert(pc110_framebuffer_width() == 640 && pc110_framebuffer_height() == 480);
    assert(pc110_get_framebuffer(machine));
    assert(atlas_pixel(0xff123456U, 0xff0000, 0xff00, 0xff) == 0x123456);
    assert(atlas_pixel(0xffff0000U, 0xf800, 0x7e0, 0x1f) == 0xf800);
    assert(atlas_pixel(0xff00ff00U, 0xf800, 0x7e0, 0x1f) == 0x7e0);
    assert(atlas_pixel(0xff0000ffU, 0xf800, 0x7e0, 0x1f) == 0x1f);
    assert(atlas_pixel(0xffffffffU, 0x7c00, 0x3e0, 0x1f) == 0x7fff);
    assert(atlas_pixel(0xff123456U, 0xff, 0xff00, 0xff0000) == 0x563412);
    pc110_destroy(machine);
    puts("Portable core boot, little-endian guest memory, and X11 pixel masks passed");
    return 0;
}
