#!/usr/bin/python3.7
from PIL import Image
import numpy as np

RED_COMP = 0
GREEN_COMP = 1
BLUE_COMP = 2


def guarantee_input(input_string, *, result_type=str, options=None):
    while True:
        response = input(input_string)
        try:
            value = result_type(response)
        except ValueError:
            print(f"{response} not a valid {result_type}")
            continue

        if options and value not in options:
            print("{response} must be one of: {options}")
        else:
            break
    return value

while True:
    name = input("Enter the name of the image to operate on: ")
    try:
        pixels = np.asarray(Image.open("./images/"+name), dtype='<i4')[:,:,:3]
        image_shape = pixels.shape
        break
    except FileNotFoundError:
        print(f"Couldn't find file {name}")

modify = input("Do you want to modify the image in any way? [Y/n]")

while modify in {"Y", "y", "yes", "Yes"}:
    print("Choose an option:")
    print("1. Apply a multiplier to a specific colour.")
    print("2. Specify a maximum or minimum value a certain colour can take.")
    print("3. Invert the colours of the image.")
    print("4. Sort all the pixels in the image.")
    print("5. Sort columns of pixels.")
    print("6. Sort rows of pixels.")

    choice = guarantee_input("> ", result_type=int, options=set(range(1,7)))

    if choice == 1:
        pixels[:,:,RED_COMP] *= guarantee_input("Red multiplier: ", result_type=int)
        pixels[:,:,GREEN_COMP] *= guarantee_input("Green multiplier: ", result_type=int)
        pixels[:,:,BLUE_COMP] *= guarantee_input("Blue multiplier: ", result_type=int)

    elif choice == 2:
        red_max = guarantee_input("Red max: ", result_type=int, options=set(range(0,256)))
        green_max = guarantee_input("Green max: ", result_type=int, options=set(range(0,256)))
        blue_max = guarantee_input("Blue max: ", result_type=int, options=set(range(0,256)))
        pixels[pixels[:,:,RED_COMP]>red_max,RED_COMP] = red_max
        pixels[pixels[:,:,GREEN_COMP]>green_max,GREEN_COMP] = green_max
        pixels[pixels[:,:,BLUE_COMP]>blue_max,BLUE_COMP] = blue_max

        red_min = guarantee_input("Red min: ", result_type=int, options=set(range(0,256)))
        green_min = guarantee_input("Green min: ", result_type=int, options=set(range(0,256)))
        blue_min = guarantee_input("Blue min: ", result_type=int, options=set(range(0,256)))
        pixels[pixels[:,:,RED_COMP]<red_min,RED_COMP] = red_min
        pixels[pixels[:,:,GREEN_COMP]<green_min,GREEN_COMP] = green_min
        pixels[pixels[:,:,BLUE_COMP]<blue_min,BLUE_COMP] = blue_min

    elif choice == 3:
        pixels = 255 - pixels

    elif choice == 4:
        red = np.sort(pixels[:,:,RED_COMP], axis=None)
        green = np.sort(pixels[:,:,GREEN_COMP], axis=None)
        blue = np.sort(pixels[:,:,BLUE_COMP], axis=None)
        pixels = np.array([red,
                           green,
                           blue]
                          ).transpose().reshape(image_shape)

    elif choice == 5:
        red = np.sort(pixels[:,:,RED_COMP].transpose())
        green = np.sort(pixels[:,:,GREEN_COMP].transpose())
        blue = np.sort(pixels[:,:,BLUE_COMP].transpose())
        pixels = np.array([red,green,blue]).transpose()

    elif choice == 6:
        red = np.sort(pixels[:,:,RED_COMP])
        green = np.sort(pixels[:,:,GREEN_COMP])
        blue = np.sort(pixels[:,:,BLUE_COMP])
        pixels = np.array([red.transpose(),
                           green.transpose(),
                           blue.transpose()]
                          ).transpose()

    np.clip(pixels, 0, 255, pixels)
    modify = input("Do you want to modify the image further? [Y/n]")

out = np.array(pixels, dtype="uint8")

print(out.shape)

final_image = Image.fromarray(out)
final_image.save("./mods/mod_" + name)
final_image.show()

