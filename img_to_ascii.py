from PIL import Image, ImageEnhance, ImageDraw, ImageFont

ascii_chars = '`$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\ '

def to_ascii_art(img, width= 1000):

    HEIGHT, WIDTH = img.size

    #adjusting the height based on width to maintain the aspect
    aspect_ratio = WIDTH/HEIGHT
    new_height = int(aspect_ratio * width)

    #RGB conversion as GIF frames use palette mode (P) which ImageEnhance can't process
    img = img.convert("RGB")

    #resize
    resized_img = img.resize(size= (width, int(new_height * 0.55)))

    #enhance
    enhancer = ImageEnhance.Sharpness(resized_img)
    res = enhancer.enhance(2) 
    enhancer = ImageEnhance.Contrast(res)
    res = enhancer.enhance(2)
    
    #grayscale
    grayscaled = res.convert("L")
    pixels = grayscaled.getdata()

    # mapping each pixel brightness (0-255) to an ascii character index
    ascii_str = "".join(ascii_chars[int((pixel / 255 ) * len(ascii_chars) - 1)] for pixel in pixels) 

    #wrapping flat ascii string into rows of 'width' characters to form a 2D grid
    art = "\n".join(ascii_str[i : i + width] for i in range(0, len(ascii_str), width))
    
    #using monospace font so that each character takes equal space
    font = ImageFont.truetype("cour.ttf", 24) 

    #measuring txt on dummy canvas to find final canvas size
    dummy_img = Image.new("RGBA", (1,1), "black")
    draw = ImageDraw.Draw(dummy_img)

    bbox = draw.textbbox((0, 0), art, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    #creating final canvas using the size from dummy canvas
    new_img = Image.new("RGBA", (text_width,text_height), "black")
    draw = ImageDraw.Draw(new_img)

    #drawing the text where canvas size == text/img size
    draw.text((0,0), art, fill="white", font=font)

    return new_img

#test and save
if __name__ == "__main__":
    path = "C:\Vscode_Python\ASCII\imgs_n_gifs\img2.jpg"
    img = Image.open(path)
    result = to_ascii_art(img)
    result.save("test.png", "PNG")
