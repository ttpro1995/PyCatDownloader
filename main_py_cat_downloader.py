import os
import requests
import shutil
import re
import argparse
import uuid

# this key is dedicate for this app only
# if you want another key, please get at https://thecatapi.com/
# do not re-use this key for your own project
dedicate_cat_api_key = "acc49791-6cc5-46c1-acf5-5e321ce201ef"
global cat_counter;


def get_json(args):
    """

    :param args: argument from arg parser
    :return:
    """
    header = {'Content-Type': 'application/json',
              'x-api-key': "acc49791-6cc5-46c1-acf5-5e321ce201ef"
              }
    limit = args.limit
    size = args.size
    rp = requests.get("https://api.thecatapi.com/v1/images/search?format=json&mime_types=png,jpg"
                      + "&limit=" + str(limit)
                      + "&size=" + str(size),
                      headers=header)
    print(rp.url)
    return rp.json()


def download_a_cat(url, dl_path):
    response = requests.get(url, stream=True)
    mime = response.headers['Content-Type']
    if "jpeg" in mime:
        fname = str(uuid.uuid4())+".jpg"
    elif "png" in mime:
        fname = str(uuid.uuid4())+".png"
    else:
        fname = str(uuid.uuid4())
    # d = response.headers['content-disposition']
    # fname = re.findall("filename=(.+)", d)
    out_file_path = os.path.join(dl_path, fname)
    with open(out_file_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def download_all_cat(js, args):
    """
    :param args:
    :return:
    """

    dl_path = args.out_dir
    if not os.path.exists(dl_path):
        os.mkdir(dl_path)

    for element in js:
        url = element['url']
        download_a_cat(url, dl_path)
        global cat_counter
        cat_counter += 1
        print("downloaded " + str(cat_counter) + " " + url)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--limit', type=int, default=25,
                        help='number of cat, max 25 per api call')
    parser.add_argument('--out_dir', type=str, default="cat_folder",
                        help='output directory')
    parser.add_argument('--size', type=str, default="full",
                        help='image size - small - med - full')
    args = parser.parse_args()
    print(args)
    global cat_counter
    cat_counter = 0

    js = get_json(args)
    download_all_cat(js, args)