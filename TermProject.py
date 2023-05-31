from tkinter import *
from tkinter import font
import tkinter.ttk
import xml.etree.ElementTree as ET
import requests

ServiceKey = 'dZcoKqxJ0w46SNHY9aMe4zgyOynLtTE0cL4fm9OOQ7oboRaunGQ09BLwKlqx1nwpH8hDfNRVFDrOOsH2Tv5jEg=='
url1 = 'https://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2'
url2 = 'https://apis.data.go.kr/1400377/forestPoint/forestPointListEmdSearch'
# url3 = 'https://apis.data.go.kr/1400000/forestStusService/getfirestatsservice'




header1 = ['이름', '주소', '높이', '소재지', '소재지 전화번호']

class MainGUI:
    def SearchName(self):
        self.EmptySearchName()
        self.name = self.SearchInput.get()
        #queryParams = {'serviceKey': ServiceKey, 'searchWrd': self.name, 'numOfRows': 3368}
        queryParams = {'serviceKey': ServiceKey, 'numOfRows': 3368}
        response = requests.get(url1, params=queryParams)
        self.root = ET.fromstring(response.text)
        for i, col_name in enumerate(header1):
            label = tkinter.Label(self.frame2, text=col_name, font=("Helvetica", 14, "bold"))
            label.grid(row=0, column=i)

        self.row_count = 1
        for item in self.root.iter("item"):
            if item.findtext("mntiname") == self.name:
                self.mntiname = item.findtext("mntiname")
                self.mntiadd = item.findtext("mntiadd")
                self.mntihigh = item.findtext("mntihigh")
                self.mntiadmin = item.findtext("mntiadmin")
                self.mntiadminnum = item.findtext("mntiadminnum")
                #self.mntidetails = item.findtext("mntidetails")
                self.mntilistno = item.findtext("mntilistno")
                self.data = [self.mntiname, self.mntiadd, self.mntihigh, self.mntiadmin, self.mntiadminnum]
                #self.data = [self.mntiname, self.mntiadd, self.mntihigh, self.mntiadmin, self.mntiadminnum, self.mntidetails]
                for i, value in enumerate(self.data):
                    label = tkinter.Label(self.frame2, text=value, font=("Helvetica", 12))
                    label.grid(row=self.row_count, column=i)
                button = tkinter.Button(self.frame2, text='숲길 정보', font=("Helvetica", 12), command=self.SearchMountainLoad(self.mntilistno))
                button.grid(row=self.row_count, column=5)
                self.row_count += 1
    def EmptySearchName(self):
        myList = self.frame2.grid_slaves()
        for i in myList:
            i.destroy()

    def SearchMountainLoad(self, listno):
        queryParams2 = {'serviceKey': ServiceKey, 'mntiListNo': listno}
        response2 = requests.get(url1, params=queryParams2)
        self.root2 = ET.fromstring(response2.text)
        label = tkinter.Label(self.frame3, text='숲길 이름', font=("Helvetica", 14, "bold"))
        label.grid(row=0, column=0)
        row_count = 1
        for item in self.root2.iter("item"):
            self.frtrlsectnnm = item.findtext("frtrlsectnnm")
            label = tkinter.Label(self.frame3, text=self.frtrlsectnnm, font=("Helvetica", 12))
            label.grid(row=row_count, column=0)
            row_count += 1


    def SearchLocation(self):
        self.EmptySearchName()
        self.location = self.LocationInput.get()
        # queryParams = {'serviceKey': ServiceKey, 'searchWrd': self.name, 'numOfRows': 3368}
        queryParams = {'serviceKey': ServiceKey, 'numOfRows': 3368}
        response = requests.get(url1, params=queryParams)
        self.root = ET.fromstring(response.text)
        for i, col_name in enumerate(header1):
            label = tkinter.Label(self.frame2, text=col_name, font=("Helvetica", 14, "bold"))
            label.grid(row=0, column=i)

        self.row_count = 1
        for item in self.root.iter("item"):
            if item.findtext("mntiadd").split()[1] == self.location:
                self.mntiname = item.findtext("mntiname")
                self.mntiadd = item.findtext("mntiadd")
                self.mntihigh = item.findtext("mntihigh")
                self.mntiadmin = item.findtext("mntiadmin")
                self.mntiadminnum = item.findtext("mntiadminnum")
                # self.mntidetails = item.findtext("mntidetails")
                self.mntilistno = item.findtext("mntilistno")
                self.data = [self.mntiname, self.mntiadd, self.mntihigh, self.mntiadmin, self.mntiadminnum]
                # self.data = [self.mntiname, self.mntiadd, self.mntihigh, self.mntiadmin, self.mntiadminnum, self.mntidetails]
                for i, value in enumerate(self.data):
                    label = tkinter.Label(self.frame2, text=value, font=("Helvetica", 12))
                    label.grid(row=self.row_count, column=i)
                button = tkinter.Button(self.frame2, text='숲길 정보', font=("Helvetica", 12),
                                        command=self.SearchMountainLoad(self.mntilistno))
                button.grid(row=self.row_count, column=5)
                self.row_count += 1

    def LikeList(self):
        pass

    def __init__(self):
        self.name = ""
        self.SearchLabel = []
        # window 생성 및 타이틀 설정
        self.window = Tk()
        self.window.title('등산 알리미')
        self.frame2 = tkinter.Frame(self.window)
        self.frame2.grid(row=0, column=1)
        self.frame3 = tkinter.Frame(self.window)
        self.frame3.grid(row=0, column=2)
        #notebook = tkinter.ttk.Notebook(window, width=800, height=600)
        #notebook.pack()
        # Main Screen
        # 제목
        self.AppNameFont = font.Font(self.window, size=32, weight='bold')
        self.AppNameLb = Label(self.window, text='등산 알리미', font=self.AppNameFont)
        self.AppNameLb.grid(row=0, column=0)

        # 이미지
        self.MainImage = PhotoImage(file='tempImage.png')
        self.MainImageLb = Label(self.window, image=self.MainImage)
        self.MainImageLb.grid(row=1, column=0)

        self.frame = Frame(self.window)
        self.frame.grid(row=2, column=0)
        #frameMtnName = Frame(window)
        #frameMtnName.pack(side='right')
        #notebook.add(frameMtnName, text='산 이름 검색')
        self.SearchNameBtn = Button(self.frame, text='산 이름 검색', command=self.SearchName)
        #Label(frameMtnName, text="페이지1의 내용", fg='red', font='helvetica 48').pack()
        self.SearchLocationBtn = Button(self.frame, text='지역 이름 검색', command=self.SearchLocation)
        self.LikeListBtn = Button(self.frame, text='즐겨찾기', command=self.LikeList)
        self.SearchInput = Entry(self.frame)
        self.LocationInput = Entry(self.frame)

        self.SearchNameBtn.grid(row=0, column=0)
        self.SearchInput.grid(row=0, column=1)
        self.SearchLocationBtn.grid(row=1, column=0)
        self.LocationInput.grid(row=1,column=1)
        self.LikeListBtn.grid(row=2, column=0)

        self.window.mainloop()


MainGUI()