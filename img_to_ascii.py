from PIL import Image, ImageEnhance, ImageDraw, ImageFont

ascii_chars = '`$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\ '

def to_ascii_art(img, width= 1000, color= "gs"):

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
    
    #checking color mode:
    if color == "gs":
        #grayscale
        grayscaled = res.convert("L")
        pixels = grayscaled.getdata()
    
    else:
        color_pixels = list(res.getdata())
        pixels = [int(0.299*r + 0.587*g + 0.114*b) for r, g, b in color_pixels]

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
    num_rows = len(art.split('\n'))

    #creating final canvas using the size from dummy canvas
    new_img = Image.new("RGBA", (text_width,text_height), "black")
    draw = ImageDraw.Draw(new_img)

    #drawing text on canvas
    if color == "gs":
        #drawing the text where canvas size == text/img size
        draw.text((0,0), art, fill="white", font=font)
    else:
        for row_idx, row in enumerate(art.split('\n')):
            for col_idx, col in enumerate(row):
                x = col_idx * (text_width / width)
                y = row_idx * (text_height / num_rows)
                r, g, b = color_pixels[row_idx * width + col_idx]
                boosted = (min(255, int(r * 3)), min(255, int(g * 3)), min(255, int(b * 3)))
                draw.text((x,y), col, fill= boosted, font=font)

    return new_img

#test and save
if __name__ == "__main__":
    path = "C:\Vscode_Python\ASCII\imgs_n_gifs\img12.jpg"
    img = Image.open(path)
    result = to_ascii_art(img, color="rgb")
    result.save("test.png", "PNG")
