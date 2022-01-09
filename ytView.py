import csv
from pprint import pprint
import youtube_dl
country = ['urlsTailand', 'urlsPoland', 'urlsIsr', 'urlsJapan']
urlsTailand = ['https://youtu.be/uRU9Lzjn8XU', 'https://youtu.be/SXKIhPWi7xQ',
               'https://youtu.be/qK5DGhrLPck', 'https://youtu.be/n6NBk8oyuVA', 'https://youtu.be/ik_OzCmB7DI', 'https://youtu.be/MNFGhVKYsCk', 'https://youtu.be/O66brml5e8o', 'https://youtu.be/S8BpDm-QPyc', 'https://youtu.be/97uCQFabFvs', 'https://youtu.be/zmjS4glmZm0', 'https://youtu.be/_mxIiEfxTxY', 'https://youtu.be/hWKuTKyP998', 'https://youtu.be/e3FX81gEtlE']
urlsPoland = ['https://youtu.be/7_2Inf7f6uQ', 'https://youtu.be/1MjgZ09l-tc', 'https://youtu.be/yoXveAEPrdA', 'https://youtu.be/y8T_CKY3naw', 'https://youtu.be/QkGrJ4ETSi0',
              'https://youtu.be/_NhFuK8jJyk', 'https://youtu.be/shT5j8RECXk', 'https://youtu.be/3IbiY7uVZHY', 'https://youtu.be/l22JmbNkFrE', 'https://youtu.be/zbH0Pw1lmdw', 'https://youtu.be/upnnFjmyT4s']
urlsIsr = ['https://youtu.be/RbYOxGqJFbE', 'https://youtu.be/5LWrzHE2gLM', 'https://youtu.be/QJvAzvtEPP4',
           'https://youtu.be/olQ3hzAEw60', 'https://youtu.be/zc06DIwAp8E', 'https://youtu.be/a70OC6XI4-4', 'https://youtu.be/1xlcleoDVa0']
urlsJapan = ['https://youtu.be/EdpCj0JlT9I', 'https://youtu.be/eM4UXSyhM_Q', 'https://youtu.be/j_iFGr1_t98', 'https://youtu.be/58wx4EChMpU', 'https://youtu.be/VzgF72eJSbg',
             'https://youtu.be/FUYtkTso88w', 'https://youtu.be/Y4Moh_DsyGQ', 'https://youtu.be/DR0n-DVu-pY', 'https://youtu.be/je5zOeAdA8s', 'https://youtu.be/4VN9FSjWBGs']


def get_video_info(youtube_url):

    with youtube_dl.YoutubeDL() as ydl:
        video_info = {}
        info = ydl.extract_info(youtube_url, download=False)
        video_info['Title'] = info.get('title')
        video_info['Views'] = info.get('view_count')
    return video_info


csvOut = 'Title;Views\n'
for url in urlsTailand:
    if __name__ == '__main__':
        video_info = get_video_info(url)
        csvOut += video_info['Title'] + ';' + str(video_info['Views']) + '\n'

f = open('D:/Documents/Data/ytInfo/tailand.txt', 'w', encoding='UTF-8')
f.write(csvOut)
f.close()

csvOut = 'Title;Views\n'
for url in urlsPoland:
    if __name__ == '__main__':
        video_info = get_video_info(url)
        csvOut += video_info['Title'] + ';' + str(video_info['Views']) + '\n'

f = open('D:/Documents/Data/ytInfo/poland.txt', 'w', encoding='UTF-8')
f.write(csvOut)
f.close()

csvOut = 'Title;Views\n'
for url in urlsIsr:
    if __name__ == '__main__':
        video_info = get_video_info(url)
        csvOut += video_info['Title'] + ';' + str(video_info['Views']) + '\n'

f = open('D:/Documents/Data/ytInfo/isr.txt', 'w', encoding='UTF-8')
f.write(csvOut)
f.close()

csvOut = 'Title;Views\n'
for url in urlsJapan:
    if __name__ == '__main__':
        video_info = get_video_info(url)
        csvOut += video_info['Title'] + ';' + str(video_info['Views']) + '\n'

f = open('D:/Documents/Data/ytInfo/japan.txt', 'w', encoding='UTF-8')
f.write(csvOut)
f.close()
