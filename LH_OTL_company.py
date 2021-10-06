    #사용 X
    def get_LH_OTL_compay(self,url):
        temp_dict = {}
        temp_list = []

        url = url +self.bidNum +'&bidDegree=' + self.bidDegree
        response = requests.get(url)

        print(url)
        if response.status_code == 200:
            html = response.text
            self.soup_obj = BeautifulSoup(html, 'html.parser')
        else : 
            print(response.status_code)

        temp = ''
        if(self.soup_obj.find('div' ,class_ = 'Lwrapper')) is not None:
            for value in self.soup_obj.find('div' ,class_ = 'Lwrapper'):
                if(value.find('thead')) != -1:
                    for tag in value.find('thead').find_all('th'):
                        if tag.text.strip() != '순번':
                            temp_list.append(tag.text.strip())
                    temp_dict['순번'] = temp_list.copy()
                temp_list.clear()
                if(value.find('tbody')) != -1:
                    for tr in value.find('tbody').find_all('tr'):
                        for i in range(1, len(tr.find_all('td'))):
                            temp_list.append(tr.find_all('td')[i].text.strip())
                        temp_dict[tr.find('td').text] = temp_list.copy()
                        temp_list.clear()
        return temp_dict