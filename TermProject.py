from tkinter import *
from tkinter import font

ServiceKey = ''


class MainGUI:
    def SearchName(self):
        pass

    def SearchLocation(self):
        pass

    def LikeList(self):
        pass

    def __init__(self):
        # window 생성 및 타이틀 설정
        window = Tk()
        window.title('등산 알리미')

        # Main Screen
        # 제목
        self.AppNameFont = font.Font(window, size=32, weight='bold')
        self.AppNameLb = Label(window, text='등산 알리미', font=self.AppNameFont)
        self.AppNameLb.pack()

        # 이미지
        self.MainImage = PhotoImage(file='tempImage.png')
        self.MainImageLb = Label(window, image=self.MainImage)
        self.MainImageLb.pack()

        frame = Frame(window)
        frame.pack()
        self.SearchNameBtn = Button(frame, text='산 이름 검색', command=self.SearchName)
        self.SearchLocationBtn = Button(frame, text='지역 이름 검색', command=self.SearchLocation)
        self.LikeListBtn = Button(frame, text='즐겨찾기', command=self.LikeList)

        self.SearchNameBtn.pack()
        self.SearchLocationBtn.pack()
        self.LikeListBtn.pack()

        window.mainloop()


MainGUI()