from tkinter import *
from tkinter import font
import tkinter.ttk
import xml.etree.ElementTree as ET
import requests

ServiceKey = 'dZcoKqxJ0w46SNHY9aMe4zgyOynLtTE0cL4fm9OOQ7oboRaunGQ09BLwKlqx1nwpH8hDfNRVFDrOOsH2Tv5jEg=='
url1 = 'https://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2'
url2 = 'https://apis.data.go.kr/1400377/forestPoint/forestPointListEmdSearch'
# url3 = 'https://apis.data.go.kr/1400000/forestStusService/getfirestatsservice'

queryParams = {'serviceKey': ServiceKey, 'pageNo': '1', 'numOfRows': '10'}
response = requests.get(url1, params=queryParams)
root = ET.fromstring(response.text)

header1 = ['mntiname', 'mntiadd', 'mntihigh', 'mntiadmin', 'mntiadminnum']

class MainGUI:
    def SearchName(self):
        for i, col_name in enumerate(header1):
            label = tkinter.Label(self.frame2, text=col_name, font=("Helvetica", 14, "bold"))
            label.grid(row=0, column=i)

        self.row_count = 1
        for item in root.iter("item"):
            self.mntiname = item.findtext("mntiname")
            self.mntiadd = item.findtext("mntiadd")
            self.mntihigh = item.findtext("mntihigh")
            self.mntiadmin = item.findtext("mntiadmin")
            self.mntiadminnum = item.findtext("mntiadminnum")

            self.data = [self.mntiname, self.mntiadd, self.mntihigh, self.mntiadmin, self.mntiadminnum]
            for i, value in enumerate(self.data):
                label = tkinter.Label(self.frame2, text=value, font=("Helvetica", 12))
                label.grid(row=self.row_count, column=i)

            self.row_count += 1
        pass

    def SearchLocation(self):
        pass

    def LikeList(self):
        pass

    def __init__(self):
        # window 생성 및 타이틀 설정
        window = Tk()
        window.title('등산 알리미')
        self.frame2 = tkinter.Frame(window)
        self.frame2.pack(side='right')
        #notebook = tkinter.ttk.Notebook(window, width=800, height=600)
        #notebook.pack()
        # Main Screen
        # 제목
        self.AppNameFont = font.Font(window, size=32, weight='bold')
        self.AppNameLb = Label(window, text='등산 알리미', font=self.AppNameFont)
        self.AppNameLb.pack()

        # 이미지
        self.MainImage = PhotoImage(file='tempImage.png')
        self.MainImageLb = Label(window, image=self.MainImage)
        self.MainImageLb.pack()

        self.frame = Frame(window)
        self.frame.pack()
        #frameMtnName = Frame(window)
        #frameMtnName.pack(side='right')
        #notebook.add(frameMtnName, text='산 이름 검색')
        self.SearchNameBtn = Button(self.frame, text='산 이름 검색', command=self.SearchName)
        #Label(frameMtnName, text="페이지1의 내용", fg='red', font='helvetica 48').pack()
        self.SearchLocationBtn = Button(self.frame, text='지역 이름 검색', command=self.SearchLocation)
        self.LikeListBtn = Button(self.frame, text='즐겨찾기', command=self.LikeList)

        self.SearchNameBtn.pack()
        self.SearchLocationBtn.pack()
        self.LikeListBtn.pack()

        window.mainloop()


MainGUI()