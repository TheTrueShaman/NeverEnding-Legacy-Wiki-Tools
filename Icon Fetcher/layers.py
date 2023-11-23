from PIL import Image, ImageChops
import icons


def get_layers(coordinates):
    img = Image.open('iconSheet.png')
    images = []
    for x, y in coordinates:
        new_image = img.crop((x * 24, y * 24, x * 24 + 24, y * 24 + 24))
        images.append(new_image)

    blank = Image.open('blank.png')
    layers = []
    for a in range(len(images)):
        icon = images[a]
        diff = ImageChops.difference(icon, blank)
        if diff.getbbox():
            icon = icon.resize((96, 96))
            layers.append(icon)
        else:
            pass
    return layers


def parse_input(layer_notation):
    split = layer_notation.lstrip("[").rstrip("]").split(",")
    temp = []
    icon_coordinates = []
    for coordinate in split:
        temp.append(int(coordinate))
        if len(temp) == 2:
            icon_coordinates.append(temp)
            temp = []
    return icon_coordinates


def layer_images(images):
    background = images[1]
    foreground = images[0]
    background.paste(foreground, (0,0), foreground.convert("RGBA"))
    background.save('./layers.png')


if __name__ == '__main__':
    icons.load_image()
    response = input("Input the layers you would like to add: ").lower()
    coordinates = parse_input(response)
    print(coordinates)
    layers = get_layers(coordinates)
    layer_images(layers)
