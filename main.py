from img_to_ascii import to_ascii_art
from PIL import Image, ImageSequence

def convert(path):
    #if uploaded file a jpg/png, call to_ascii_art
    if path.endswith((".jpg", ".png")):
        img = Image.open(path)
        result = to_ascii_art(img)
        result.save("result.png", "PNG")

    #extract frames if .gif, call to_ascii_art
    elif path.endswith(".gif"):
        frames_list = [] ## collecting ascii frames
        with Image.open(path) as im:
            for frame in ImageSequence.Iterator(im):
                frames_list.append(to_ascii_art(frame, width = 300))

            #save
            frames_list[0].save(
                "result.gif",
                save_all=True,
                append_images=frames_list[1:],
                duration=41, #1000/24 = 41ms = 24fps
                loop=0  #infinite loop
                )
    #if not a gif or png/jpg       
    else:
        print("unsupported format")

if __name__ == "__main__":
    convert("imgs_n_gifs/gifs/gif3.gif")