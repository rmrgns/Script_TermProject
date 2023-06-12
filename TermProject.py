from tkinter import *
from tkinter import font
from tkintermapview import TkinterMapView
import tkinter.messagebox
import tkinter.ttk
import xml.etree.ElementTree as ET
import requests

ServiceKey = 'dZcoKqxJ0w46SNHY9aMe4zgyOynLtTE0cL4fm9OOQ7oboRaunGQ09BLwKlqx1nwpH8hDfNRVFDrOOsH2Tv5jEg=='
url1 = 'https://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2'
url2 = 'https://apis.data.go.kr/1400377/forestPoint/forestPointListEmdSearch'
# url3 = 'https://apis.data.go.kr/1400000/forestStusService/getfirestatsservice'




header1 = ['이름', '주소', '높이', '소재지', '소재지 전화번호', '상세정보']


class MainGUI:
    def SearchName(self):
        self.SearchListBox.delete(0, END)
        self.MntList = []
        self.name = self.SearchInput.get()
        queryParams = {'serviceKey': ServiceKey, 'searchWrd': self.name, 'numOfRows': 3368}
        #queryParams = {'serviceKey': ServiceKey, 'numOfRows': 3368}
        response = requests.get(url1, params=queryParams)
        self.root = ET.fromstring(response.text)


        self.row_count = 1
        for item in self.root.iter("item"):
            #if item.findtext("mntiname") == self.name:
            self.mntiname = item.findtext("mntiname")
            self.mntiadd = item.findtext("mntiadd")
            self.mntihigh = item.findtext("mntihigh")
            self.mntiadmin = item.findtext("mntiadmin")
            self.mntiadminnum = item.findtext("mntiadminnum")
            self.mntidetails = item.findtext("mntidetails")
            self.mntitop = item.findtext("mntitop")
            self.SearchListBox.insert(self.row_count, self.mntiname)
            self.MntList.append([self.mntiname, self.mntiadd, self.mntihigh, self.mntiadmin, self.mntiadminnum, self.mntidetails, self.mntitop])
            self.row_count += 1


    def SearchMnt(self):
        self.RenderText.configure(state='normal')
        self.RenderText.delete(0.0, END)
        self.LbIndex = self.SearchListBox.curselection()[0]

        mnti = self.MntList[self.LbIndex]

        # 설명 텍스트 변경
        self.RenderText.insert(INSERT, '이름: ')
        self.RenderText.insert(INSERT, mnti[0])
        self.RenderText.insert(INSERT, '\n')
        self.RenderText.insert(INSERT, '주소: ')
        self.RenderText.insert(INSERT, mnti[1])
        self.RenderText.insert(INSERT, '\n')
        self.RenderText.insert(INSERT, '높이: ')
        self.RenderText.insert(INSERT, mnti[2])
        self.RenderText.insert(INSERT, '\n')
        self.RenderText.insert(INSERT, '소재지: ')
        self.RenderText.insert(INSERT, mnti[3])
        self.RenderText.insert(INSERT, '\n')
        self.RenderText.insert(INSERT, '소재지 전화번호')
        self.RenderText.insert(INSERT, mnti[4])
        self.RenderText.insert(INSERT, '\n')
        self.RenderText.insert(INSERT, '상세정보: ')
        self.RenderText.insert(INSERT, mnti[5])
        self.RenderText.insert(INSERT, '\n')
        self.RenderText.insert(INSERT, '봉우리 정보: ')
        self.RenderText.insert(INSERT, mnti[6])
        self.RenderText.insert(INSERT, '\n')

        self.RenderText.configure(state='disabled')

        # 맵 위치 변경
        address = mnti[0]
        self.map_widget.set_address(address, marker=True)

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

    def ShowMap(self):
        self.map_widget = TkinterMapView(width=400, height=550, corner_radius=0)
        self.map_widget.pack()
        self.map_widget.place(x=780, y=25)
        self.map_widget.set_address("Seoul")
        # self.search_marker = self.map_widget.set_address("Seoul", marker=True)

    def InitSearchListBox(self):
        ListBoxScrollbar = Scrollbar(self.window)
        ListBoxScrollbar.pack()
        ListBoxScrollbar.place(x=625, y=50)

        self.SearchListBox = Listbox(self.window, font=("Helvetica", 12), activestyle='none', width=20, height=5, borderwidth=10,
                                relief='ridge', yscrollcommand=ListBoxScrollbar.set)

        #self.SearchListBox.insert(1,'empty')

        self.SearchListBox.pack()
        self.SearchListBox.place(x=420, y=50)

        ListBoxScrollbar.config(command=self.SearchListBox.yview)

    def InitRenderText(self):
        RenderTextScrollbar = Scrollbar(self.window)
        RenderTextScrollbar.pack()
        RenderTextScrollbar.place(x=625,y=150)

        self.RenderText = Text(self.window, width=45, height=30, borderwidth=10, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
        self.RenderText.pack()
        self.RenderText.place(x=420, y=180)
        RenderTextScrollbar.config(command=self.RenderText.yview)
        RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

        self.RenderText.configure(state='disabled')

    def __init__(self):
        self.name = ""
        self.SearchLabel = []
        # window 생성 및 타이틀 설정
        self.window = Tk()
        self.window.title('등산 알리미')
        self.window.geometry('1250x600')

        self.MntList = []

        #notebook = tkinter.ttk.Notebook(window, width=800, height=600)
        #notebook.pack()
        # Main Screen
        # 제목
        self.AppNameFont = font.Font(self.window, size=32, weight='bold')
        self.AppNameLb = Label(self.window, text='등산 알리미', font=self.AppNameFont)
        self.AppNameLb.pack()
        self.AppNameLb.place(x=125, y=0)

        # 이미지
        self.MainImage = PhotoImage(file='tempImage.png')
        self.MainImageLb = Label(self.window, image=self.MainImage)
        self.MainImageLb.pack()
        self.MainImageLb.place(x=0, y=50)

        self.frame = Frame(self.window)
        self.frame.pack()
        self.frame.place(x=0, y=400)
        #frameMtnName = Frame(window)
        #frameMtnName.pack(side='right')
        #notebook.add(frameMtnName, text='산 이름 검색')
        self.SearchNameBtn = Button(self.frame, text='산 이름 검색', command=self.SearchName)
        self.SearchLocationBtn = Button(self.frame, text='지역 이름 검색', command=self.SearchLocation)
        self.LikeListBtn = Button(self.frame, text='즐겨찾기', command=self.LikeList)
        self.SearchInput = Entry(self.frame)
        self.LocationInput = Entry(self.frame)

        self.SearchNameBtn.grid(row=0, column=0)
        self.SearchInput.grid(row=0, column=1)
        self.SearchLocationBtn.grid(row=1, column=0)
        self.LocationInput.grid(row=1, column=1)
        self.LikeListBtn.grid(row=2, column=0)

        #for i, col_name in enumerate(header1):
        #    label = tkinter.Label(self.frame2, text=col_name, font=("Helvetica", 14, "bold"))
        #    label.grid(row=0, column=i)
        self.label = Label(self.window, text='이름', font=("Helvetica", 14, "bold"))
        self.label.pack()
        self.label.place(x=500, y=10)
        self.SearchListboxBtn = Button(self.window, font=60, text='검색', command=self.SearchMnt)
        self.SearchListboxBtn.pack()
        self.SearchListboxBtn.place(x=700, y=100)
        self.InitSearchListBox()
        self.InitRenderText()
        self.ShowMap()

        self.window.mainloop()


MainGUI()
