from tkinter import *
from tkinter import font
from tkintermapview import TkinterMapView
import tkinter.messagebox
import tkinter.ttk
import xml.etree.ElementTree as ET
import requests
import spam

ServiceKey = 'dZcoKqxJ0w46SNHY9aMe4zgyOynLtTE0cL4fm9OOQ7oboRaunGQ09BLwKlqx1nwpH8hDfNRVFDrOOsH2Tv5jEg=='
url1 = 'https://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2'
url2 = 'https://apis.data.go.kr/1400377/forestPoint/forestPointListSidoSearch'
# url3 = 'https://apis.data.go.kr/1400000/forestStusService/getfirestatsservice'

class MainGUI:
    def SearchName(self):
        self.searchType = 0
        self.SearchListBox.delete(0, END)
        self.MntList = []
        self.name = self.SearchInput.get()
        queryParams = {'serviceKey': ServiceKey, 'searchWrd': self.name}
        response = requests.get(url1, params=queryParams)
        self.root = ET.fromstring(response.text)

        self.row_count = 0
        for item in self.root.iter("item"):
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

        # spam모듈을 활용한 검색 결과 개수 출력
        self.UseModule()

    def SearchMnt(self):
        self.RenderText.configure(state='normal')
        self.RenderText.delete(0.0, END)
        self.LbIndex = self.SearchListBox.curselection()[0]

        if self.searchType == 0:
            mnti = self.MntList[self.LbIndex]
        elif self.searchType == 1:
            mnti = self.likelist[self.LbIndex]

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
        self.RenderText.insert(INSERT, '\n\n')
        self.RenderText.insert(INSERT, '상세정보: ')
        self.RenderText.insert(INSERT, mnti[5])
        self.RenderText.insert(INSERT, '\n\n')
        self.RenderText.insert(INSERT, '봉우리 정보: ')
        self.RenderText.insert(INSERT, mnti[6])
        self.RenderText.insert(INSERT, '\n')

        self.RenderText.configure(state='disabled')

        # 맵 위치 변경
        mntiaddress = mnti[1].split()[0] + ' ' + mnti[1].split()[1]
        address = mntiaddress + ' ' + mnti[0]
        self.map_widget.set_address(mnti[1], marker=True)
        self.map_widget.set_address(mnti[0], marker=True)
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
        self.searchType = 0
        self.location = self.LocationInput.get()
        queryParams = {'serviceKey': ServiceKey, 'numOfRows': 3368}
        response = requests.get(url1, params=queryParams)
        self.root = ET.fromstring(response.text)

        self.row_count = 0
        for item in self.root.iter("item"):
            if item.findtext("mntiadd").split()[1] == self.location:
                self.mntiname = item.findtext("mntiname")
                self.mntiadd = item.findtext("mntiadd")
                self.mntihigh = item.findtext("mntihigh")
                self.mntiadmin = item.findtext("mntiadmin")
                self.mntiadminnum = item.findtext("mntiadminnum")
                self.mntidetails = item.findtext("mntidetails")
                self.mntitop = item.findtext("mntitop")
                self.SearchListBox.insert(self.row_count, self.mntiname)
                self.MntList.append(
                    [self.mntiname, self.mntiadd, self.mntihigh, self.mntiadmin, self.mntiadminnum, self.mntidetails,
                     self.mntitop])
                self.row_count += 1

        self.UseModule()

    def CheckForestPoint(self):
        self.locationName = self.ForestPointInput.get()
        locationNum = 0
        if self.locationName == "서울특별시":
            locationNum = 11
        elif self.locationName == "부산광역시":
            locationNum = 26
        elif self.locationName == "대구광역시":
            locationNum = 27
        elif self.locationName == "인천광역시":
            locationNum = 28
        elif self.locationName == "광주광역시":
            locationNum = 29
        elif self.locationName == "대전광역시":
            locationNum = 30
        elif self.locationName == "울산광역시":
            locationNum = 31
        elif self.locationName == "세종특별자치시":
            locationNum = 36
        elif self.locationName == "경기도":
            locationNum = 41
        elif self.locationName == "강원도":
            locationNum = 42
        elif self.locationName == "충청북도":
            locationNum = 43
        elif self.locationName == "충청남도":
            locationNum = 44
        elif self.locationName == "전라북도":
            locationNum = 45
        elif self.locationName == "전라남도":
            locationNum = 46
        elif self.locationName == "경상북도":
            locationNum = 47
        elif self.locationName == "경상남도":
            locationNum = 48
        elif self.locationName == "제주특별자치도":
            locationNum = 50
        else:
            print("error")
            return

        self.ForestPointName.configure(text=self.locationName)

        queryParams = {'serviceKey': ServiceKey,'numOfRows': 10, 'pageNo': 1, 'localAreas': locationNum}
        response = requests.get(url2, params=queryParams)
        self.root = ET.fromstring(response.text)

        self.d1 = 0.00001
        self.d2 = 0.00001
        self.d3 = 0.00001
        self.d4 = 0.00001

        for item in self.root.iter("item"):
            date = item.findtext("analdate")
            self.d1 += int(item.findtext("d1"))
            self.d2 += int(item.findtext("d2"))
            self.d3 += int(item.findtext("d3"))
            self.d4 += int(item.findtext("d4"))
            #print(date)

        self.UseGraph()

    def UseGraph(self):
        c2 = Canvas(self.window, width=400, height=300)
        c2.pack()
        c2.place(x=1200,y=100)
        data = [self.d1, self.d2, self.d3, self.d4]
        data2 = ['낮음', '다소높음', '높음', '매우높음']
        start = 0
        s = sum(data)

        for i in range(4):
            extent = data[i] / s * 360
            c2.create_arc((0, 0, 300, 300), fill=self.color[i], outline='white', start=start, extent=extent)
            start = start + extent
            c2.create_rectangle(300, 20 + 20 * i, 300 + 30, 20 + 20 * (i + 1), fill=self.color[i])
            c2.create_text(300 + 70, 10 + 20 * (i + 1), text=str(data2[i]))

    def UseModule(self):
        count = 0
        count = spam.numOfResult(self.MntList)
        self.numOfResult.configure(text=count)

    def ShowMap(self):
        self.map_widget = TkinterMapView(width=400, height=550, corner_radius=0)
        self.map_widget.pack()
        self.map_widget.place(x=780, y=25)
        self.map_widget.set_address("Seoul")
        # self.search_marker = self.map_widget.set_address("Seoul", marker=True)

    def InitSearchListBox(self):
        ListBoxScrollbar = Scrollbar(self.window)
        ListBoxScrollbar.pack(side=RIGHT, fill=BOTH)
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

    def LikeList(self):
        self.searchType = 1
        self.SearchListBox.delete(0, END)
        for i in range(len(self.likelist)):
            self.SearchListBox.insert(i, self.likelist[i][0])


    def AddLikeList(self):
        if self.searchType == 1:
            return
        self.LbIndex = self.SearchListBox.curselection()[0]
        if self.MntList[self.LbIndex][0] == '':
            #print('empty list')
            return
        mnti = self.MntList[self.LbIndex]
        for i in self.likelist:
            if mnti == i:
                return
        self.likelist.append([mnti[0], mnti[1], mnti[2], mnti[3], mnti[4], mnti[5], mnti[6]])
        print(self.likelist)

    def DeleteLikeList(self):
        if self.searchType == 0:
            return
        self.LbIndex = self.SearchListBox.curselection()[0]
        if self.likelist[self.LbIndex][0] == '':
            return
        self.likelist.pop(self.LbIndex)
        self.LikeList()



    def __init__(self):
        self.name = ""
        self.SearchLabel = []
        # window 생성 및 타이틀 설정
        self.window = Tk()
        self.window.title('등산 알리미')
        self.window.geometry('1650x600')

        self.MntList = []
        self.color = []
        self.color.append('#88AAAA')
        self.color.append('#AAAAAA')
        self.color.append('#CCAAAA')
        self.color.append('#FFAAAA')
        self.searchType = 0
        self.likelist = []

        #notebook = tkinter.ttk.Notebook(window, width=800, height=600)
        #notebook.pack()
        # Main Screen
        # 제목
        self.AppNameFont = font.Font(self.window, size=32, weight='bold')
        self.AppNameLb = Label(self.window, text='등산 알리미', font=self.AppNameFont)
        self.AppNameLb.pack()
        self.AppNameLb.place(x=100, y=0)

        # 이미지
        self.MainImage = PhotoImage(file='mntscreen.png')
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
        self.ForestPointBtn = Button(self.frame, text='예보 지역', command=self.CheckForestPoint)
        self.ForestPointInput = Entry(self.frame)

        self.ForestPointInput.grid(row=3, column=1)
        self.ForestPointBtn.grid(row=3, column=0)
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
        self.SearchListboxBtn.place(x=675, y=80)
        self.InitSearchListBox()
        self.InitRenderText()
        self.ShowMap()
        self.numOfResultLb = Label(self.window, text='검색 결과', font=("Helvetica", 14, "bold"))
        self.numOfResultLb.pack()
        self.numOfResultLb.place(x=665, y=10)
        self.numOfResult = Label(self.window, text='0', font=("Helvetica", 14, "bold"))
        self.numOfResult.pack(side="right")
        self.numOfResult.place(x=690, y=35)
        self.ForestPointName = Label(self.window, text='지역 이름', font=("Helvetica", 14, "bold"))
        self.ForestPointName.pack()
        self.ForestPointName.place(x=1250,y=50)
        self.AddLikeListBtn = Button(self.window, font=30, text='즐겨찾기 추가', command=self.AddLikeList)
        self.AddLikeListBtn.pack()
        self.AddLikeListBtn.place(x=640, y=115)
        self.DelLikeListBtn = Button(self.window, font=30, text='즐겨찾기 삭제', command=self.DeleteLikeList)
        self.DelLikeListBtn.pack()
        self.DelLikeListBtn.place(x=640, y=145)

        self.window.mainloop()


MainGUI()
