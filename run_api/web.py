import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
from urllib.parse import urlencode, quote_plus
import re
from requests.models import Response


if __name__ == '__main__':
    bidnum = 'EA20212948'
    degree = '01'
    query = f'?biNo={bidnum}({degree})'

    url = 'https://ebid.etri.re.kr/ebid/index.do'

    response = requests.get(url)

    header = response.headers

    cookie = header['Set-Cookie']

    headerr = {'Cookie': cookie}
    url = 'https://ebid.etri.re.kr/ebid/ebid/ebidCustInfoResultView.do' + query
    response_result = requests.get(url, headers=headerr)

    if response.status_code == 200:
        html = response_result.text
        soup_obj = BeautifulSoup(html, 'html.parser')
    else:
        print(response.status_code)

    # for i in range(1, 3):
        # print(soup_obj.find_all('table', id='table01')[i].find_all('td'))

    for value in soup_obj.find_all('table', id='table01'):
        label = value.find('td', class_='name02').text.strip()
        print(label)

