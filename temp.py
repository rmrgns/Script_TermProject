
import requests
import xml.etree.ElementTree as ET
import tkinter
#병원정보 서비스 예제
url = 'https://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2'
# 공공데이터포털에서 발급받은 디코딩되지 않은 인증키 입력
service_key = 'dZcoKqxJ0w46SNHY9aMe4zgyOynLtTE0cL4fm9OOQ7oboRaunGQ09BLwKlqx1nwpH8hDfNRVFDrOOsH2Tv5jEg=='
queryParams = {'serviceKey': service_key, 'pageNo': '1', 'numOfRows': '10'}

response = requests.get(url, params=queryParams)
print(response.text)
root = ET.fromstring(response.text)

window = tkinter.Tk()
window.title("병원정보")

frame = tkinter.Frame(window)
frame.pack()

header = ['Mntiname', 'Mntiadd', 'Mntihigh', 'Mntiadmin', 'Mntiadminnum']

for i, col_name in enumerate(header):
    label = tkinter.Label(frame, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=0, column=i)

row_count = 1
for item in root.iter("item"):
    mntiname = item.findtext("mntiname")
    mntiadd = item.findtext("mntiadd")
    mntihigh = item.findtext("mntihigh")
    mntiadmin = item.findtext("mntiadmin")
    mntiadminnum = item.findtext("mntiadminnum")

    data = [mntiname, mntiadd, mntihigh, mntiadmin, mntiadminnum]
    for i, value in enumerate(data):
        label = tkinter.Label(frame, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=i)

    row_count += 1

window.mainloop()
