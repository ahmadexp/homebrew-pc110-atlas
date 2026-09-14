#ifndef PC110_UNIX_PIXEL_H
#define PC110_UNIX_PIXEL_H
#include <stdint.h>

/* Convert numeric ARGB to the X visual's masks. Never reinterpret host bytes. */
static unsigned long atlas_channel(unsigned int value, unsigned long mask) {
    unsigned int shift = 0;
    unsigned long maximum;
    if (!mask) return 0;
    while (((mask >> shift) & 1UL) == 0) ++shift;
    maximum = mask >> shift;
    return (((value * maximum + 127UL) / 255UL) << shift) & mask;
}

static unsigned long atlas_pixel(uint32_t argb, unsigned long red,
                                 unsigned long green, unsigned long blue) {
    return atlas_channel((argb >> 16) & 255U, red)
        | atlas_channel((argb >> 8) & 255U, green)
        | atlas_channel(argb & 255U, blue);
}
#endif
