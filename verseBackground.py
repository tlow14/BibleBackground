import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import ctypes

#TODO:
#Add options menu include,  location of text, type of background, size of background, font type

def grab_html(website):
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_verse_from_html(soup):
    verseElement = soup.find(class_="verse-wrapper").next_element
    verse = verseElement.get_text()
    verse = verse.replace('\n', ' ')
    verseReference = verseElement.nextSibling.get_text()

    newVerse = ""
    verseReference = verseReference[:-6]
    while len(verse) >= 80:
        #Makes sure to break at the end of a space
        i = 79
        while verse[i] != ' ':
            i = i - 1
        #needed to get rid of the space
        i = i + 1


        newVerse = newVerse + verse[:i] + '\n'
        verse = verse[i:]
    newVerse = newVerse + verse + '\n' + verseReference
    return newVerse

def get_picture_random():
    randomUrl = "https://source.unsplash.com/random/3840x2160/?mountain,water"
    response = requests.get(randomUrl)
    data = response.url

    return data



def save_image(img_url, verse):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))

    fileLocation = "C:\\Users\\tomlo\\Downloads\\Unsplash Photos\\background.jpg"

    draw = ImageDraw.Draw(img)

    # create font object with the font file and specify
    # desired size

    font = ImageFont.truetype('.\\BebasNeue-Regular.ttf', size=60)

    #TODO: FIX THIS PARTs
    #Chooses the color that will be different from the background
    imageColor = img.convert("RGB")
    origianlX = 1000
    origianlY = 200
    pixelX = origianlX
    pixelY = origianlY
    maxY = 750 + ((int(len(verse) / 80)) + 1) * 50
    pixelRed = 0
    pixelGreen = 0
    pixelBlue = 0
    count = 1
    while pixelX <= origianlX + 1250:
        while pixelY <= origianlX + maxY:
            pixelVal = imageColor.getpixel((pixelX, pixelY))
            pixelRed = pixelRed + pixelVal[0]
            pixelGreen = pixelGreen + pixelVal[1]
            pixelBlue = pixelBlue + pixelVal[2]
            pixelY = pixelY + 50
            count = count + 1

        pixelY = 0
        pixelX = pixelX + 25

    pixelRed = pixelRed / count
    pixelBlue = pixelBlue / count
    pixelGreen = pixelGreen / count

    luma = 1 - ((0.299 * pixelRed) + (0.587 * pixelBlue) + (0.114 * pixelGreen)) / 255
    color = 'rgb(0, 0, 0)' if luma < .5 else 'rgb(255, 255, 255)'
    stroke_color = 'rgb(0, 0, 0)' if luma > .5 else 'rgb(255, 255, 255)'
    (x, y) = (origianlX, origianlY)

    # draw the message on the background
    draw.text((x, y), verse, fill=color, font=font, stroke_width=1, stroke_fill=stroke_color)

    # save the edited image
    # save a image using extension
    img.save(fileLocation)
    set_background(fileLocation)


def set_background(fileLocation):
    # This sets the background
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, fileLocation, 0)


if __name__ == '__main__':
    bibleHtml = grab_html("https://www.bible.com/verse-of-the-day")
    verse = get_verse_from_html(bibleHtml)
    picture_url = get_picture_random()
    save_image(picture_url, verse)
    print(verse)
