import requests, bs4, json, os

def get_info(id:int):
    html = requests.get(f"https://www.pixiv.net/artworks/{id}").content
    soup = bs4.BeautifulSoup(html, "html.parser")
    info_json = soup.find("meta",id="meta-preload-data")["content"]
    info = json.loads(info_json)
    urls = []
    original_url:str = info["illust"][str(id)]["userIllusts"][str(id)]["url"].replace("https://i.pximg.net/c/250x250_80_a2/img-master/img/","https://i.pximg.net/img-original/img/").replace("_square1200.jpg",".jpg")
    pageCount:int = info["illust"][str(id)]["userIllusts"][str(id)]["pageCount"]
    for i in range(pageCount):
        urls.append(original_url.replace("p0",f"p{i}"))
    return urls,pageCount

def get_original_pic(url:str,id:int,pageCount:int):
    header = {"Host":"i.pximg.net",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
            "Accept":"image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Encoding":"gzip, deflate, br, zstd",
            "Referer":"https://www.pixiv.net/"}
    res = requests.get(url,headers=header)
    with open(f"./{id}/p{pageCount}.jpg",'wb') as f:
        f.write(res.content)
    return

def download(id:int):
    urls,pageCount=get_info(id)
    os.mkdir(str(id))
    for i in range(pageCount):
        get_original_pic(urls[i],id,i)
