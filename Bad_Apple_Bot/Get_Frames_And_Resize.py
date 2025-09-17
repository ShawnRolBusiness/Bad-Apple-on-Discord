import os

import cv2
from PIL import Image

# Put file path of the video here.
file_path = "Bad_Apple.mp4"

# Max width while retaining aspect ratio.
width: int = 50

# Set to a lower value if you want a shorter video.
max_frame_count: int = 9999999

ASCII_CHARS = [".", ".", ",", "-", ":", ";", "+", "?", "#", "&", "$"]


# STEP 1: GET FRAMES FROM VIDEO
def get_frames_from_video(path):
    video = cv2.VideoCapture(path)
    count: int = 0

    while True:
        if count <= max_frame_count:
            print("GETTING FRAME: " + str(count))
            true, image = video.read()
            try:
                cv2.imwrite("images/frame%d.jpg" % count, image)
                count += 1

            except Exception as e:
                print(e)
                break
        else:
            break



# STEP 2: RESIZE IMAGE AND GRAYSCALE IMAGE
def resize(frame, new_width:width, count):
    original_width, original_height = frame.size
    aspect_ratio = original_height / original_width
    new_height = int(new_width * aspect_ratio)
    resized_image = frame.resize((new_width, new_height)).convert("L")
    resized_image.save("images/frame" + str(count) + ".jpg")



# STEP 3: LASTLY, WRITE PIXELS TO ASCII CHARACTERS
def pixels_to_ascii(image, count):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    pixel_count = len(characters)
    frame = "\n".join(characters[i:(i+width)] for i in range(0, pixel_count, width))
    with open("text/frame" + str(count) + ".txt", "w") as f:
        print(frame)
        f.write(frame)
    f.close()



# MAIN ENTRY POINT
def main() -> None:
    get_frames_from_video(file_path)

    for i in range(len(os.listdir("images"))):
        resize(Image.open("images/frame" + str(i) + ".jpg"), width, i)
        pixels_to_ascii(Image.open("images/frame" + str(i) + ".jpg"), i)

    print("DONE")


if __name__ == '__main__':
    main()
