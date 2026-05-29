from img_to_ascii import to_ascii_art
from PIL import Image, ImageSequence

def convert(path, width, color):
    #if uploaded file a jpg/png, call to_ascii_art
    if path.endswith((".jpg", ".png")):
        img = Image.open(path)
        result = to_ascii_art(img= img, width= 1000, color= color)
        result.save("result.png", "PNG")

    #extract frames if .gif, call to_ascii_art
    elif path.endswith(".gif"):
        frames_list = [] ## collecting ascii frames
        with Image.open(path) as im:
            for frame in ImageSequence.Iterator(im):
                frames_list.append(to_ascii_art(img= frame, width = width, color= color))

            #save
            frames_list[0].save(
                "result.gif",
                save_all=True,
                append_images=frames_list[1:],
                duration=66, #1000/15 = 66ms = 15fps
                loop=0  #infinite loop
                )
    #if not a gif or png/jpg       
    else:
        print("unsupported format")

if __name__ == "__main__":
    convert(path= "C:\Vscode_Python\ASCII\imgs_n_gifs\img5.jpg", width= 400, color="rgb")
