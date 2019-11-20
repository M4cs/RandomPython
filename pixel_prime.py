# This takes each prime number and sees if any digits 0-9 are missing from it, if so it assigns it a color and adds it to the pixel array. Silly script


from PIL import Image
import numpy as np
import json
from tqdm import trange

with open('results.json', 'r+') as json_f:
    numbs = json.load(json_f)
color_code = {
    0: (0,0,0),
    1: (255,0,0),
    2: (255,127,0),
    3: (255, 255, 0),
    4: (0, 255, 0),
    5: (0, 0, 255),
    6: (46, 43, 95),
    7: (139, 0, 255),
    8: (150, 175, 85),
    9: (80, 45, 150)
}

def generate_primes():
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1

pixels = []
fresh = []
bn = 0

for i in generate_primes():
    print('Generating For Prime In Position {}'.format(bn), end='\r')
    if bn == 1080:
        break
    if len(fresh) >= 1920:
        pixels.append(fresh)

    for x in range(0, 9):
        if str(x) not in str(i):
            fresh.append(color_code[x])
    bn += 1

array = np.array(pixels, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.save('new.png')
