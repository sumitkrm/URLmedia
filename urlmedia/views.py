from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def index(request):
    return render(request, 'index.html')

def tracker(request):
    url = request.GET.get('text', 'default')
    checkbox = request.GET.get('checkbox', False)
    r = requests.get(url, stream=True)
    if checkbox:
        if 'png' in url or 'jpg' in url or 'jpeg' in url:
            with open('urlmedia/static/img.jpg','wb') as f:
                f.write(r.content)
            media = 'img.png'
            params = {'url':url, 'media':media}
            return render(request, 'tracker.html',params)

        elif 'pdf' in url:
            with open("urlmedia/static/new_file.pdf", "wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
            return render(request, 'tracker.html')
        else:
            download_video_series(get_video_links(r, url))
            return render(request, 'tracker.html')



def download(request):
    return render(request, 'download.html')


def get_video_links(r, url):
    soup = BeautifulSoup(r.content, 'html5lib')
    links = soup.findAll('a')
    video_links = [url + link['href'] for link in links if link['href'].endswith('mp4')]
    return video_links


def download_video_series(video_links):
    for link in video_links:
        file_name = link.split('/')[-1]
        r = requests.get(link, stream=True)

        # download started
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    return