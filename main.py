import os
from glob import glob

from PIL import Image, ImageFilter


BLEED_PX = 200


def expand(bbox, amount):
    return (bbox[0] - amount, bbox[1] - amount, bbox[2] + amount, bbox[3] + amount)


def crop(image_path):
    im = Image.open(image_path)
    gray = im.convert('L')

    # Pre-process mask
    gray2 = gray.filter(ImageFilter.MaxFilter(size=11))
    bw = gray2.point(lambda x: 0 if x > 150 else 255, '1')

    bbox = expand(bw.getbbox(), BLEED_PX)
    # TODO make sure box is square-ish
    cropped = im.crop(box=bbox)

    size = (bbox[2] - bbox[0]) // 2, (bbox[3] - bbox[1]) // 2
    final = cropped.resize(size, resample=Image.LANCZOS)
    return final


if __name__ == '__main__':
    if not os.path.isdir('output'):
        os.mkdir('output')

    for original in glob('input/*.JPG'):
        fn, ext = os.path.splitext(os.path.basename(original))
        new_fn = 'output/{}.cropped.jpg'.format(fn)
        if os.path.isfile(new_fn):
            continue

        print(original)
        new_image = crop(original)
        new_image.save(new_fn)
