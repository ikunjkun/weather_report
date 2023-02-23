from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class App:
    def __init__(self):
        self.location =[]
        self.window=Tk()
        self.window.iconphoto(False, PhotoImage(file='./img/title.gif'))
        self.window.title('天气预报')
        width=800
        height=700
        left=(self.window.winfo_screenwidth()-width)/2
        top=(self.window.winfo_screenheight()-height)/2   
        self.window.geometry('%dx%d+%d+%d'%(width,height,left,top))
        self.window.resizable(False,False)
        self.cerate_widgets()
        self.cerate_widgets()
        self.set_widgets()
        self.show_local_weather()
        mainloop()
        
    def refresh_weather(self):
        for frame in self.frame_list:
            self.note.forget(frame)
        for city in self.location:
            self.get_city_weather(self.loca_p[self.location.index(city)],city)

    def cerate_widgets(self):
        self.note=ttk.Notebook()
        self.f1 = ttk.Frame()
        self.tree=ttk.Treeview(self.f1)
        self.menu=Menu(self.window)
        self.window['menu']=self.menu
        self.menu1=Menu(self.menu,tearoff=False)
        self.menu2=Menu(self.menu,tearoff=False)
        self.menu3=Menu(self.menu,tearoff=False)
        self.weather_image={}
        self.frame_list=[]

    def set_widgets(self):
        self.location=[]
        self.loca_p = []
        style = ttk.Style(self.window)
        style.theme_use("default")
        style.configure("Treeview",rowheight=40,
                        background="#87CEEA",
                        fieldbackground="#87CEEA", foreground="white")
        self.menu.add_cascade(label='开始',menu=self.menu1)
        self.menu1.add_command(label='其他',command='')
        self.menu2.add_command(label='刷新',command=lambda:self.refresh_weather())
        self.menu1.add_separator()
        self.menu1.add_command(label='退出',command=self.quit_window)
        self.menu.add_cascade(label='操作',menu=self.menu2)
        self.menu2.add_command(label='添加城市',command=lambda:self.import_city())
        self.menu2.add_command(label='其他',command='')
        self.menu.add_cascade(label='关于',menu=self.menu3)
        self.menu3.add_command(label='其他',command='')

    def show_local_weather(self):
        response = requests.get('https://api64.ipify.org?format=json').json()
        ip = str(response["ip"])
        url = "https://restapi.amap.com/v3/ip?ip="+ip+"&output=xml&key=edcdc07cd21b7d132db19be121ca8b2c"
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text,"xml")
        self.local_province=soup.province.string
        self.local_city=soup.city.string[:-1]
        self.get_city_weather(self.local_province,self.local_city)
        self.location.append(self.local_city)
  
    def quit_window(self):
        ret=messagebox.askyesno('退出','是否要退出？')
        if ret:
            self.window.destroy()

    def import_city(self):
        self.t=Toplevel()
        self.t.resizable(0,0)
        width=300
        height=150
        left=(self.t.winfo_screenwidth()-width)/2
        top=(self.t.winfo_screenheight()-height)/2
        self.t.geometry('%dx%d+%d+%d'%(width,height,left,top))
        self.t.title('选择城市')
        self.tl1=ttk.Label(self.t,text='请选择城市：')
        self.tl1.pack()
        province_list = []
        self.f=Frame(self.t)
        self.f.pack(pady=10)
        for province in city_list:
            if province == "Adm1_Name_ZH":
                continue
            province_list.append(province)
        ttk.Label(self.f,text="选择省份").grid(row=0, sticky=W)
        ttk.Label(self.f,text="选择市").grid(row=1, sticky=W)
        self.tc1=ttk.Combobox(self.f,justify='center',state='readonly',value=province_list)
        self.tc2=ttk.Combobox(self.f,justify='center',state='readonly')
        self.tc1.grid(row=0, column=1, sticky=E)
        self.tc1.bind('<<ComboboxSelected>>',self.show_tc2_value)
        self.tc2.grid(row=1, column=1, sticky=E)
        self.tb1=ttk.Button(self.t,text='选择',command=lambda :self.select_city(self.tc1.get(),self.tc2.get()))
        self.tb1.pack(pady=10)

    def show_tc2_value(self,event):
        self.tc2.config(value=[])
        province=self.tc1.get()
        cities = []
        for city in city_list[province]:
            cities.append(city)
        self.tc2.config(value=cities)

    def select_city(self,province,city_name):
        flag = 0
        for city in city_list[province]:
            if city_name==city:
                flag = 1
                if city in self.location:
                    messagebox.showwarning('警告','此城市已添加，请勿重复添加！')
                else:
                    self.location.append(city)
                    self.get_city_weather(province,city)
                    self.t.destroy()              
        if flag == 0:
            messagebox.showwarning('警告','城市输入错误，请重新输入！')

    def get_city_weather(self,province,city_name):
        self.loca_p.append(province)
        url='https://free-api.qweather.com/v7/weather/7d?location='+city_list[province][city_name] +'&key=e82f7fb43bdb4bb480c6a8fea0ff945a'
        response = requests.get(url)
        res = response.json()
        result = res["daily"]
        data = {}
        for each in result:
            date = each['fxDate']
            data[date]={}
            data[date]["weather"] = each["textDay"]
            data[date]["max_temperature"] = each["tempMax"]
            data[date]["min_temperature"] = each["tempMin"]
        self.show_city_weather(data,city_name)
   
    def show_city_weather(self,city_data,city_name):
        self.weather_image[city_name] = []
        self.frame= Frame(self.window,takefocus=True)
        self.note.add(self.frame, text=city_name)
        self.frame_list.append(self.frame)
        self.note.place(x=0,y=0,width=800,height=700)
        self.tree = ttk.Treeview(self.frame)
        self.tree["columns"] = ("weather","min_temperature","max_temperature")
        self.tree.column('#0',anchor=CENTER,minwidth=60,width=70)
        self.tree.column(column='#0',anchor=CENTER,minwidth=60,width=70)
        self.tree.column(column='#1',anchor=CENTER,minwidth=95,width=110)
        self.tree.column(column='#2',anchor=CENTER,minwidth=90,width=100)
        self.tree.column(column='#3',anchor=CENTER,minwidth=95,width=110)
        self.tree.heading(column='#0',text='天气')
        self.tree.heading(column='#1', text='最低气温')
        self.tree.heading(column='#2', text='最高气温')
        self.tree.heading(column='#3', text='日期')
        self.tree.place(x=0,y=0,width=800,height=250)
        self.tree.tag_configure("evenColor",background="lightblue")
        i = 0
        for date in city_data:
            self.weather_image[city_name].append(PhotoImage(file="./img/"+img_list[city_data[date]["weather"]]+".png"))
            if i%2 == 1:
                self.tree.insert('', i,text=city_data[date]["weather"],image=self.weather_image[city_name][i],
                                 values=(city_data[date]["min_temperature"]+"℃",
                                city_data[date]["max_temperature"]+"℃",date),tags=("evenColor") )
            else:
                self.tree.insert('', i,text=city_data[date]["weather"],image=self.weather_image[city_name][i],
                                 values=(city_data[date]["min_temperature"]+"℃",
                                city_data[date]["max_temperature"]+"℃",date))
            i += 1
        self.draw_line_char(city_data,city_name)
           
    def draw_line_char(self,city_data,city_name):
        self.canvas=Canvas(self.frame,width=800,height=400,bg="#87CEEA")
        self.canvas.place(x=0,y=250)
        self.canvas.create_line(100,350,700,350,width=2,dash=(5,1))
        date_list =[]
        max_temperature_scaled =[]
        min_temperature_scaled =[]
        min_temperature_text = []
        max_temperature_text = []
        min_list = []
        max_list = []
        weather_list = []
        for date in city_data:
            date_list.append(date)
            weather_list.append(city_data[date]["weather"])
            max_list.append(int(city_data[date]["max_temperature"]))
            min_list.append(int(city_data[date]["min_temperature"]))
        min_min_t=min(min_list)
        for i in range(7):
            max_y=max_list[i]-min_min_t
            min_y=min_list[i]-min_min_t
            x=100+(i+1)*80
            max_temperature_scaled.append((x,220-(7.5*max_y)))
            min_temperature_scaled.append((x,220-(7.5*min_y))) 
        self.canvas.create_line(max_temperature_scaled,fill='red')
        self.canvas.create_line(min_temperature_scaled,fill='yellow')
        self.week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
        for i in range(8):
            x=100+(i*80)
            if i!= 0:
                self.canvas.create_line(x,350,x,345,width=2)
                self.canvas.create_text(x,349,text=date_list[i-1],anchor=N)
                self.canvas.create_text(x,280,text=weather_list[i-1],anchor=N)
                week_index = datetime.strptime(date_list[i-1],"%Y-%m-%d").weekday()
                self.canvas.create_text(x,310,text=self.week_list[week_index],anchor=N)
                self.canvas.create_image(x-7,250,anchor='nw',image=self.weather_image[city_name][i-1])
        i=0
        for x,y in max_temperature_scaled:
            self.canvas.create_oval(x-4,y-4,x+4,y+4,width=1,outline='black',fill='red')
            self.canvas.create_text(x,y-15,text=max_list[i],fill='red')
            i+=1
        i=0
        for x,y in min_temperature_scaled:
            self.canvas.create_oval(x-4,y-4,x+4,y+4,width=1,outline='black',fill='yellow')
            self.canvas.create_text(x,y-15,text=min_list[i],fill='yellow')
            i+=1
     
with open('city_list1.json','r') as f1:
    city_list = json.load(f1)
with open('picture_list.json','r') as f2:
    img_list = json.load(f2)
a=App()
