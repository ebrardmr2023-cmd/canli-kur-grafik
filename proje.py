import http.client
import json
import os 
import sqlite3
from datetime  import datetime
import tkinter as tk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 074ZtHTPalELy7NXDmwaJf:0F7CjRaTBMKuRgeQAwMkFk"
    }

conn.request("GET", "/economy/currencyToAll?int=10&base=TRY", headers=headers)

res = conn.getresponse()
data = res.read()
veri = json.loads(data.decode("utf-8"))
print(data.decode("utf-8"))
print(json.dumps(veri, indent=4, ensure_ascii=False))# bu komutu yapay zekayadan aldım.

dizin = os.path.dirname(os.path.abspath(__file__))
veritabani_yolu = os.path.join(dizin, "data.db")

baglanti = sqlite3.connect(veritabani_yolu, isolation_level = None)# autocommit
cur = baglanti.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Kurlar(BirimID INTEGER PRIMARY KEY, tarih TEXT, birim TEXT, oran REAL)")# oranın real olması gerektiğini bir web siteden öğrendim.

liste = []
anlikZaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for doviz in veri["result"]["data"]:
    birim = doviz["code"]
    oran = float(doviz["rate"])
    liste.append((anlikZaman, birim, oran))# çift parantez kullanmam gerektiğini yapay zekadan aldım.
cur.executemany("INSERT INTO Kurlar(tarih, birim, oran) VALUES(?,?,?)",liste)
cur.close()
baglanti.close()

def sDoviz(secilenDoviz):# veritabanından veri çekmek için bir fonksiyon oluşturmam gerektiğini yapay zekadan aldım.Komutu( fonksiyonu) ben oluşturdum.
    print(f"arayüzden secilen döviz kurları: {secilenDoviz}" )
    for widget in pencere.winfo_children():# for döngüsünü yapay zekadan aldım.
        if not isinstance(widget, tk.Menu):
            widget.destroy()
    vtBaglanti = sqlite3.connect(veritabani_yolu, isolation_level=None)#autocommit
    vtCur = vtBaglanti.cursor()
    vtCur.execute("SELECT tarih, oran FROM Kurlar WHERE birim = ? ORDER BY tarih ASC", (secilenDoviz,))
    veriler = vtCur.fetchall()
    vtCur.close()
    vtBaglanti.close()
    tarihler = [satir[0] for satir in veriler]# bu listeleri de web sitesinden aldım.
    oranlar = [satir[1] for satir in veriler]
    print(oranlar)
    print(tarihler)
    fig = Figure(figsize=(10, 8))# figür yapısı oluşturmayı da yapay zekadan aldım.
    ax1 = fig.add_subplot(211)# değişkenleri ben oluşturdum.
    ax2 = fig.add_subplot(212)
    ax1.plot(tarihler, oranlar,color="blue", marker="o", label="kur değişimi")
    ax1.legend()
    ax2.bar(tarihler, oranlar, color="red", label="dönemsel hacim/değer")
    ax2.legend()
    fig.autofmt_xdate()# bu iki komut da yapay zekadan.
    fig.tight_layout()# bu iki komut da yapay zekadan.
    canvas = FigureCanvasTkAgg(fig, master=pencere)# matplotlibi tkintere bağlamayı yapay zekadan aldım.
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand="True")

pencere = tk.Tk()
pencere.title("döviz takip programı")
pencere.geometry("800x600")
menuCubugu = tk.Menu(pencere)
dovizMenusu = tk.Menu(menuCubugu, tearoff=0)
dovizMenusu.add_command(label="dolar(USD)", command= lambda: sDoviz("USD"))
dovizMenusu.add_command(label="Euro(EUR)", command= lambda: sDoviz("EUR"))
dovizMenusu.add_command(label="Sterlin(GBP)", command= lambda: sDoviz("GBP"))
dovizMenusu.add_command(label="Frank(CHF)", command= lambda: sDoviz("CHF"))
dovizMenusu.add_command(label="Japon Yeni(JPY)", command= lambda: sDoviz("JPY"))
dovizMenusu.add_command(label="Suudi Riyali(SAR)", command= lambda: sDoviz("SAR"))
dovizMenusu.add_command(label="İran Riyali(IRR)", command= lambda: sDoviz("IRR"))
menuCubugu.add_cascade(label=" DÖVİZ BİRİMLERİ", menu=dovizMenusu)
pencere.config(menu=menuCubugu)
pencere.mainloop()