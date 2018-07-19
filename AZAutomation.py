import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import threading

Large_Font = ("Verdana", 12)
project_entry = 0

class AZauto(tk.Tk):

    def __init__(self, *args, **kwargs):
    
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "A-Z Automation")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageMenu):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    def checkEntry(self, cont, count):
        frame = self.frames[StartPage]
        try:
            count = int(count)
        except:
            messagebox.showerror("Error", "Must use a whole number")
            frame.project_entry.delete(0,100)
            return
        if count % 25 != 0:
            messagebox.showerror("Error", "Please use a number divisible by 25")
            return
        frame = self.frames[cont]
        frame.tkraise()
        t = threading.Thread(target = self.loopPages, args = [count])
        t.start()

    def saveMenu(self, cont,  PageWaitTime, User, Password):
        frame = self.frames[cont]
        with open(r'C:\Program Files\SiteEdge\Settings.txt', 'r+') as json_file:
            data = json.load(json_file)
            for p in data['Menu']:
                p['WaitTimeOut'] = PageWaitTime
                p['UserName'] = User
                p['Password'] = Password
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()
        frame.tkraise()

    def loopPages(self, count):
        frame = self.frames[PageOne]
        if count > 1000:
            loopCount = 40
            downloadCount = count/1000
        else:
            loopCount = count/25
            downloadCount = 1
        i = 0
        j = 0

        while downloadCount >= 0 and j < 40:
            j = j + 1
            while loopCount >= 1 and i <= count-25:
                if pausePage == True:
                    print("TRUE pausePage")
                try:
                    driver.find_element_by_id("checkall").click()
                    print(i)
                except:
                    time.sleep(2)
                    driver.find_element_by_id("checkall").click()
                    print("timed out")
                time.sleep(2.75)
                try:
                    driver.find_element_by_id("span_next_button_upper").click()
                except:
                    time.sleep(1.25)
                    driver.find_element_by_id("span_next_button_upper").click()
                time.sleep(1.25)
                i = i + 25
                loopCount = loopCount - 1
                frame.progressBar.step(100/(count/25))
                PageOne.updateLabel(self, i)
                if i > 10000:
                    break
            if count-i>1000:
                loopCount = 40
            else:
                loopCount = (count-i)/25
            driver.execute_script("document.getElementsByClassName('ui-button-text')[5].click()")
            time.sleep(1)
            try: 
                driver.find_element_by_id("_customName").send_keys("AtoZ_" + str(j))
                print(j)
            except:
                time.sleep(1)
                driver.find_element_by_id("_customName").send_keys("AtoZ_" + str(j))
            driver.find_element_by_id("download_level_detail1").click()
            Click Button
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[9]/div[11]/div/button[2]/span').click()
            time.sleep(8)
            driver.refresh()
            time.sleep(3)
            downloadCount = downloadCount - 1
            PageOne.updateLabel2(self, j)
        self.frames[PageTwo].tkraise()

    def quit(self):
        app.destroy()
        driver.quit()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.label = tk.Label(self, text="Number of Leads:", font=Large_Font)
        self.label.pack(pady=(10,0),padx=(36))
        self.project_entry = ttk.Entry(self, width=30)
        self.project_entry.pack()

        button1 = ttk.Button(self, width=20, text="Run", command=lambda: controller.checkEntry(PageOne, self.project_entry.get()))
        button1.pack(pady=(2,2))

        button2 = ttk.Button(self, width=20, text="Settings", command=lambda: controller.show_frame(PageMenu))
        button2.pack(pady=(2, 8))        

    
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.progressBar = ttk.Progressbar(self, length=300, mode='determinate')
        self.progressBar.pack(padx=5, pady=5)

        self.label = ttk.Label(self, text="Preparing to run...")
        self.label.pack(pady=(0,3))
        self.label2 = ttk.Label(self, text="")
        self.label2.pack(pady=(0,8))

        buttonPause = ttk.Button(self, width=15, text="Pause", command=lambda: print("Pause Pressed"))
        buttonPause.pack()

    def updateLabel(self, i):
        self.frames[PageOne].label['text'] = 'Number of Leads: ' + str(i)
        self.frames[PageOne].update()

    def updateLabel2(self, j):
        self.frames[PageOne].label2['text'] = 'Documents downloaded ' + str(j) 
        self.frames[PageOne].update()

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Completed", font=Large_Font)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Finish", command=lambda: controller.quit())
        button1.pack()

class PageMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        labelStartPage = tk.Label(self, text="Starting Page:", font=Large_Font)
        labelStartPage.pack(pady=10,padx=10)

        self.entryStartPage = ttk.Entry(self, width=6)
        self.entryStartPage.insert(0, "0")
        self.entryStartPage.pack()
        
        label = tk.Label(self, text="WaitTimeOut:", font=Large_Font)
        label.pack(pady=10,padx=10)

        self.entryPageMenu = ttk.Entry(self, width=6)
        self.entryPageMenu.insert(0, WaitTimeOut)
        self.entryPageMenu.pack()

        labelUser = ttk.Label(self, text="Username:", font=Large_Font)
        labelUser.pack()

        self.entryUser = ttk.Entry(self, width=15)
        self.entryUser.insert(0, UserName)
        self.entryUser.pack()

        labelPassword = ttk.Label(self, text="Password:", font=Large_Font)
        labelPassword.pack()

        self.entryPassword = ttk.Entry(self, width=15)
        self.entryPassword.insert(0, Password)
        self.entryPassword.pack()
    
        
        button1 = tk.Button(self, text="Save", command=lambda: controller.saveMenu(StartPage, self.entryPageMenu.get(), self.entryUser.get(), self.entryPassword.get()))
        button1.pack()

        buttonCancel = tk.Button(self, text="Cancel", command=lambda: controller.show_frame(StartPage))
        buttonCancel.pack()

def main():
        controller.show_frame(StartPage)

        
pausePage = False

driver = webdriver.Chrome(r"C:\Program Files\SiteEdge\chromedriver.exe")
driver.set_page_load_timeout(60)
driver.get("https://www.atozdatabases.com/patronsignin")

#Get JSON File
with open(r'C:\Program Files\SiteEdge\Settings.txt', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for p in data['Menu']:
        WaitTimeOut = p['WaitTimeOut']
        UserName = p['UserName']
        Password = p['Password']
try:
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div/div[1]/div/a').click()
    driver.find_element_by_id("login-username").send_keys(UserName)
    driver.find_element_by_id("login-password").send_keys(Password)
except:
    print("make sure you are on the correct network")

app = AZauto()
app.mainloop()
    
