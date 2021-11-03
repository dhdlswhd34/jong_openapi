
    # 입찰공고 데이터
    # def get_ETRI_announce(self, url):

    #     # 쿠키 가져오기
    #     if self.get_ETRI_cookie() is False:
    #         return False

    #     response = requests.get(url, headers=self.header)

    #     if response.status_code == 200:
    #         html = response.text
    #         self.soup_obj = BeautifulSoup(html, 'html.parser')
    #     else:
    #         print(response.status_code)

    #     if (self.soup_obj.find_all('table', id='table01')) is not None:
    #         i = 0
    #         result_dic = {}
    #         for value in self.soup_obj.find_all('table', id='table01'):
    #             j = 0
    #             temp_arr = []
    #             item_arr = []
    #             item_dic = {}
    #             if (i == an.공고번호정보):    # 공고번호 정보
    #                 item_arr = []
    #                 # key값 가져오기
    #                 for body in value.find_all('td', class_='name02'):
    #                     item_arr.append(self.strip_re(body))
    #                 # value값 가져오기
    #                 for body in value.find_all('td', class_=''):
    #                     if j >= 14:
    #                         if(j == 16):
    #                             temp_arr.append(self.strip_re(body))
    #                             result_dic[item_arr[14]] = {}
    #                             result_dic[item_arr[14]][item_arr[15]] = temp_arr
    #                             temp_arr = []
    #                         elif(j == 19):
    #                             temp_arr.append(self.strip_re(body))
    #                             result_dic[item_arr[14]][item_arr[16]] = temp_arr
    #                         else:
    #                             temp_arr.append(self.strip_re(body))
    #                         j += 1
    #                     else:
    #                         result_dic[item_arr[j]] = self.strip_re(body)
    #                         j += 1
    #             if(i == an.입찰일정):     # 입찰 일정
    #                 result_dic['입찰일정'] = []
    #                 # key값 가져오기
    #                 for body in value.find_all('td', class_='list01'):
    #                     temp_arr.append(self.strip_re(body))
    #                 # value값 가져오기
    #                 for body in value.find_all('td', class_=''):
    #                     if(j == len(temp_arr) - 1):
    #                         item_dic[temp_arr[j]] = self.strip_re(body)
    #                         j = 0
    #                         item_arr.append(item_dic)
    #                         result_dic['입찰일정'].append(item_arr)
    #                         item_dic = {}
    #                         item_arr = []
    #                     else:
    #                         item_dic[temp_arr[j]] = self.strip_re(body)
    #                         j += 1
    #             if(i == an.입찰참고사항):     # 입찰참고사항
    #                 result_dic[value.find('td', class_='name02').text.strip()] = value.find('textarea').text.strip()
    #             if(i == an.가격정보):     # 가격정보
    #                 result_dic['가격정보(단위:원)'] = {}
    #                 # key값 가져오기
    #                 for body in value.find_all('td', class_='name02'):
    #                     temp_arr.append(self.strip_re(body))
    #                 # value값 가져오기
    #                 for body in value.find_all('td', class_=''):
    #                     if(j == (len(temp_arr) - 1)):
    #                         item_dic[temp_arr[j]] = self.strip_re(body)
    #                         result_dic['가격정보(단위:원)'] = item_dic
    #                     else:
    #                         item_dic[temp_arr[j]] = self.strip_re(body)
    #                         j += 1
    #             if(i >= an.적격심사세부기준) and len(value.find_all('td', class_='name02')) > 1:     # 적격심사 세부기준
    #                 result_dic['적격심사 세부기준'] = []
    #                 # key값 가져오기
    #                 for body in value.find_all('td', class_='name02'):
    #                     temp_arr.append(self.strip_re(body))
    #                 # value값 가져오기
    #                 for body in value.find_all('td', class_=''):
    #                     if(j == (len(temp_arr) - 1)):
    #                         item_dic[temp_arr[j]] = self.strip_re(body)
    #                         j = 0
    #                         item_arr.append(item_dic)
    #                         result_dic['적격심사 세부기준'].append(item_arr)
    #                         item_dic = {}
    #                         item_arr = []
    #                     else:
    #                         item_dic[temp_arr[j]] = self.strip_re(body)
    #                         j += 1
    #             if(i >= an.입찰공고안내서류) and (value.find_all('td', class_='list01')) is not None:     # 입찰공고안내서류
    #                 result_dic['입찰공고안내서류'] = []
    #                 # key값 가져오기
    #                 for body in value.find_all('td', class_='list01'):
    #                     temp_arr.append(self.strip_re(body))
    #                 # value값 가져오기
    #                 for body in value.find_all('td', class_=''):
    #                     if(j == (len(temp_arr) - 1)):
    #                         item_dic[temp_arr[j]] = self.strip_re(body)
    #                         item_dic['URL'] = self.get_etri_file(body.find('a'))
    #                         j = 0
    #                         item_arr.append(item_dic)
    #                         result_dic['입찰공고안내서류'].append(item_arr)
    #                         item_dic = {}
    #                         item_arr = []
    #                     else:
    #                         item_dic[temp_arr[j]] = self.strip_re(body)
    #                         j += 1
    #             i += 1
    #     return result_dic




    # def get_ETRI_result(self, url):
    #     # 쿠키 가져오기
    #     if self.get_ETRI_cookie() is False:
    #         return False

    #     # 쿠키 넣어주기
    #     response = requests.get(url, headers=self.header)

    #     if response.status_code == 200:
    #         html = response.text
    #         self.soup_obj = BeautifulSoup(html, 'html.parser')
    #     else:
    #         print(response.status_code)

    #     if (self.soup_obj.find('table', id='table01')) is not None:
    #         i = 0
    #         result_dic = {}
    #         for value in self.soup_obj.find_all('table', id='table01'):
    #             j = 0
    #             temp_arr = []
    #             item_arr = []
    #             item_dic = {}
    #             if (i == rn.최종결과):    # 최종결과
    #                 for body in value.find_all('td'):
    #                     # key값 가져오기
    #                     if j == 0:
    #                         temp = self.strip_re(body)
    #                         j = 1
    #                     # value값 가져오기
    #                     else:
    #                         result_dic[temp] = self.strip_re(body)
    #                         j = 0
    #             if (i == rn.복수예비가격):    # 복수 예비가격 및 예정가격
    #                 for body in value.find_all('tr'):
    #                     # key값 가져오기
    #                     if body.find('td', class_='name02') is None:
    #                         i += 1
    #                         break
    #                     # value값 가져오기
    #                     if j == 0:
    #                         for item in body.find_all('td'):
    #                             result_dic[item.text.strip()] = []
    #                         j = 1
    #                     elif j == 1:
    #                         for item in body.find_all('td')[0:-1]:
    #                             result_dic['복수예비가격'].append(item.text.strip())
    #                         item_arr.append(body.find_all('td', class_='list01')[0].text.strip())
    #                         item_arr.append(body.find_all('td', class_='list01')[-1].text.strip())
    #                         result_dic['추첨결과 및 예정가격'].append(item_arr)
    #                         item_arr = []
    #             if (i == rn.개찰결과):    # 개찰결과
    #                 result_dic['개찰결과'] = []
    #                 # key값 가져오기
    #                 for body in value.find_all('td', class_='list01'):
    #                     temp_arr.append(self.strip_re(body))
    #                 # value값 가져오기
    #                 for body in value.find_all('td', class_=''):
    #                     if (j == (len(temp_arr) - 1)):
    #                         item_dic[temp_arr[j]] = self.strip_re(body)
    #                         j = 0
    #                         item_arr.append(item_dic)
    #                         result_dic['개찰결과'].append(item_arr)
    #                         item_dic = {}
    #                         item_arr = []
    #                     else:
    #                         item_dic[temp_arr[j]] = self.strip_re(body)
    #                         j += 1
    #             i += 1
    #     else:
    #         return False
    #     return result_dic


        # 파일 체크
    def check_ETRI_query_data(self, type):
        self.bidunm_degree = []

        # 1:입찰공고 2:개찰결과 3:견적문의 4:견적결과
        list_arr = []
        if(type == 1):
            txt = 'etri_announce.txt'
        elif(type == 2):
            txt = 'etri_result.txt'
        elif(type == 3):
            txt = 'etri_cust.txt'
        elif(type == 4):
            txt = 'etri_cust_result.txt'

        # 마지막 데이터 불러오기
        f = open(f'{txt}', 'rt', encoding='UTF8')
        while True:
            line = f.readline()
            if not line:
                break
            line = line.split(',')
            list_arr.append(line)
        f.close()

        # 추가 내용 저장
        f = open(f'{txt}', 'a+', encoding='UTF8')
        for pg in self.result_arr:
            for bs in pg:
                i = 1
                for txt in list_arr:
                    if(txt[0:4] == bs):     # 중복체크
                        i = 0   # 중복인 경우 0
                        break   # 발견시 break
                if(i == 1):     # 새로운 데이터 저장
                    current_time = datetime.now()
                    f.write(f'{bs[0]},{bs[1]},{bs[2]},{bs[3]},{current_time}\n')    #저장 (ex. 공고번호(차수),입찰시작일,입찰종료일,진행상태,현재시각 )
                    self.bidunm_degree.append([bs[0], bs[3]])   # 새로운 리스트 공고번호 저장
        f.close()