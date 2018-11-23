import pandas
import requests
from bs4 import BeautifulSoup
import hashlib
import imgurpython
from urllib.parse import unquote

#imgur = imgurpython.ImgurClient("8855661c8ddf300", "b227d17afa10e056f1a9eb9788e3b634c1a4fb3a")

def download_file(url):
    file_type_parts_one = url.split("?")
    file_type_parts = file_type_parts_one[0].split(".")
    file_type = file_type_parts[len(file_type_parts) - 1]
    url.encode('ISO-8859-1')
    file_name = "images/" + hashlib.md5(url.encode("utf8")).hexdigest() + "." + file_type
    r = requests.get(url)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return file_name

def get_ebay_images(body):
    bs = BeautifulSoup(body, features="html.parser")
    images = []
    for cell in bs.find_all(class_="tdThumb"):
        img = cell.find("img")
        src_raw = img.get("src")
        src = src_raw.replace("s-l64.", "s-l1600.")
        images.append(src)
    return images


def get_imgur_album_images(url):
    parts_one = url.split("?")
    url_parts = parts_one[0].strip("/").split("/")
    album_id = url_parts[len(url_parts) - 1]
    images = []
    for img in imgur.get_album_images(album_id):
        images.append(img.link)
    return images

def get_imgur_gallery_images(url):
    parts_one = url.split("?")
    url_parts = parts_one[0].strip("/").split("/")
    gallery_id = url_parts[len(url_parts) - 1]
    images = []
    for img in imgur.gallery_item(gallery_id).images:
        images.append(img['link'])
    return images

def get_imgur_image(url):
    parts_one = url.split("?")
    url_parts = parts_one[0].strip("/").split("/")
    image_id = url_parts[len(url_parts) - 1]
    image = imgur.get_image(image_id)
    return image.link


image_urls = []
legit_status = []
image_location = []




df = pandas.read_csv("hockey_jerseys.csv")
count = 0
for i, url, legit in df.itertuples(index=False):
    if legit == 1 and url.find("rover.ebay.com") != -1:
        count = count + 1
    continue
    if True:

        if url.find("rover.ebay.com") != -1:
            continue # Skip because it's a pain
        r = requests.get(url, allow_redirects=False)
        r.encoding = 'ISO-8859-1'
        if r.status_code == 200:
            print(url)
            if url.find("ebay") != -1:
                for src in get_ebay_images(r.text):
                    downloaded_file = download_file(src)
                    image_location.append(downloaded_file)
                    image_urls.append(src)
                    legit_status.append(legit)
            elif url.find("i.imgur") != -1:
                downloaded_file = download_file(url)
                image_location.append(downloaded_file)
                image_urls.append(url)
                legit_status.append(legit)
            elif url.find("imgur.com/a/") != -1:
                for src in get_imgur_album_images(url):
                    downloaded_file = download_file(src)
                    image_location.append(downloaded_file)
                    image_urls.append(src)
                    legit_status.append(legit)
            elif url.find("imgur.com/gallery/") != -1:
                for src in get_imgur_gallery_images(url):
                    downloaded_file = download_file(src)
                    image_location.append(downloaded_file)
                    image_urls.append(src)
                    legit_status.append(legit)
            elif url.find("imgur.com") != -1:
                src = get_imgur_image(url)
                downloaded_file = download_file(src)
                image_location.append(downloaded_file)
                image_urls.append(src)
                legit_status.append(legit)
            count = count + 1

#new_df = pandas.DataFrame({"url": image_urls, "legit": legit_status, "file":image_location} )

#new_df.to_csv("hockey_jerseys_processed.csv")
print(count)