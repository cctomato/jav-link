from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sys
import urllib.parse

findLink = re.compile(r'<a alt="(.*?)"')
findMagnet = re.compile(r'<a href="(.*?)"')
findPage = re.compile(r'>\n(.*?)\n</a>')
findSize = re.compile(r'<td class="whitespace-nowrap pl-4 text-right text-sm text-gray-400 font-mono">(.*?)</td>')

def main(name):
    baseurl = "https://thisav.com/dm18/actresses/" + urllib.parse.quote(name) + "?filters=individual"
    print(baseurl)
    data_list = getData(baseurl)
    saveData(data_list, name)

def saveData(datalist, name):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet(name, cell_overwrite_ok=True)
    col = ("number", "link", "size")
    for i in range(0, 3):
        sheet.write(0, i, col[i])
    for i in range(0, len(datalist)):
        data = datalist[i]
        for j in range(0, 3):
            sheet.write(i+1, j, data[j])
    book.save(name + ".xls")

def getVideoData(number):
    data_list = []
    maxSize = 0
    magnet = 'none'
    url = 'https://thisav.com/dm18/' + number
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('tbody', class_="divide-y divide-gray-500"):
        item = str(item)
        tdSoup = BeautifulSoup(item, "html.parser")
        for tr in tdSoup.find_all('tr'):
            tr = str(tr)
            link = str(re.findall(findMagnet, tr)[0])
            size = str(re.findall(findSize, tr)[0])
            if len(link) > 2 and len(size) > 2:
                size_number = size[:-2]
                if size[-2:] == 'MB':
                    size = round(float(size_number) / 1024, 2)
                else:
                    size = float(size_number)
                if size > maxSize:
                    maxSize = size
                    magnet = link
    data_list.append(number)
    data_list.append(magnet)
    data_list.append(maxSize)
    print(number, magnet, maxSize)
    return data_list

def getData(baseurl):
    data_list = []
    totalPage = 1
    index = 0;
    totalHtml = askURL(baseurl)
    totalSoup = BeautifulSoup(totalHtml, "html.parser")
    pageArray = totalSoup.find_all('a', class_="relative inline-flex items-center px-4 py-2 -ml-px text-sm font-medium text-nord4 leading-5 rounded-lg hover:bg-nord1 focus:z-10 focus:outline-none active:bg-nord1 transition ease-in-out duration-150")
    lastHtml = pageArray[-1:][0]
    page = re.findall(findPage, str(lastHtml))
    if len(page) > 0:
        totalPage = int(page[0])
    for i in range(1, int(totalPage)+1):
        url = baseurl + "&page=" + str(i)
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('a', class_="text-secondary group-hover:text-primary"):
            item = str(item)
            link = re.findall(findLink, item)
            if len(link) > 0:
                video_list = getVideoData(link[0])
                if len(video_list) > 0:
                    data_list.append(video_list)
                    index = index + 1
    print("total video is ", index)
    return data_list

def askURL(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        print("error")
    return html

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('please enter name')
    else:
        main(sys.argv[1])
