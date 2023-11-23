# import os
import requests
from PIL import Image, ImageChops


def load_image():
    image_location = 'https://orteil.dashnet.org/legacy/img/iconSheet.png?v=1'
    image = requests.get(url=image_location, stream=True)
    with open('iconSheet.png', 'wb') as sheet:
        sheet.write(image.content)


def crop_images():
    img = Image.open('iconSheet.png')
    images = []
    for a in range(32):
        for b in range(32):
            new_image = img.crop((b*24, a*24, b*24+24, a*24+24))
            images.append(new_image)

    blank = Image.open('blank.png')
    icon_amount = 0
    for a in range(len(images)):
        # os.remove('./icons/icon' + str(a) + '.png')
        icon = images[a]
        diff = ImageChops.difference(icon, blank)
        if diff.getbbox():
            icon = icon.resize((96, 96))
            icon.save('./icons/icon' + str(icon_amount) + '.png')
            icon_amount += 1
        else:
            pass


if __name__ == '__main__':
    load_image()
    crop_images()
