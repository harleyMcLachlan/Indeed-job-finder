import tkinter as tk
import time
import webbrowser
from langdetect import detect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import customtkinter as ctk
from webdriver_manager.chrome import ChromeDriverManager

##################### JOB FINDING ########################################

### closes popups if possible
def closePopups(driver):
    try:
        closes = driver.find_elements(By.CLASS_NAME,"icl-CloseButton")
        if len(closes) > 0:
            for close in closes:
                close.click()
    except:
        pass
    
    try:
        closes = driver.find_elements(By.ID,"onetrust-reject-all-handler")
        if len(closes) > 0:
            for close in closes:
                close.click()
    except:
        pass

    try:
        closes = driver.find_elements(By.CSS_SELECTOR,"button[aria-label='schließen']")
        if len(closes) > 0:
            for close in closes:
                close.click()
    except:
        pass

    try:
        closes = driver.find_elements(By.CSS_SELECTOR,"button[aria-label='close']")
        if len(closes) > 0:
            for close in closes:
                close.click()
    except:
        pass
    

###Get list of jobs on page            
def getJobs(driver,window):
    closePopups(driver)
    jobList = driver.find_elements(By.XPATH,"/html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul/li")
    #Get job snippet text
    for jobListing in jobList:
        snippets = jobListing.find_elements(By.CLASS_NAME,"job-snippet")
        for snippet in snippets:
            #detect language
            try:
                if detect(snippet.text) == "en":
                    #if language is english, print the title
                    titles = jobListing.find_elements(By.CLASS_NAME,"jobTitle")
                    for title in titles:
                        #filter out words
                        if any(substring.lower() in title.text.lower() for substring in filteredWordList):
                            continue
                        links = jobListing.find_elements(By.CLASS_NAME,"jcs-JobTitle")
                        for link in links:
                            jobTitle = trimStrLen(title.text,70)

                            #check links for already seen jobs
                            if any(alreadyOpenedLink in jobTitle for alreadyOpenedLink in alreadySearchedJobsList):
                                window.my_frame.createBtn(jobTitle,link.get_attribute('href'),True)
                            else:
                                window.my_frame.createBtn(jobTitle,link.get_attribute('href'))
                                file.write(jobTitle + "\n")     
    
            except:
                pass
                    
### goes to next page of jobs if possible
def nextPage(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.2)
    pages = driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Next Page']")
    if len(pages) == 0:
        return 0
    for page in pages:
        try:
            page.click()
        except:
            time.sleep(0.5)
            closePopups(driver)
            page.click()
        elem=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"job-snippet")))
    return 1

### Main call to populate screen with jobs
def populateJobs(driver,window):
    #OPENS indeed to engineer jobs in berlin last 24 hours
    driver.get("https://de.indeed.com/jobs?q=engineer&l=Berlin&fromage=1&vjk=0a4a7664e5720982")

    getJobs(driver,window)
    while(not(debug) and nextPage(driver)):
       getJobs(driver,window)
    time.sleep(0.5)
    window.labels[0].configure(text="Results: " + str(window.my_frame.numRows))
    driver.close()

def trimStrLen(str,len=50):
    return str[:len]

### callback function for button
def btnCall(btn,url):
    openLink(url)
    btn.configure(fg_color="grey")

def xBtnCall(btn):
    btn.configure(fg_color="transparent")

### opens link in default browser
def openLink(url):
    webbrowser.open(url, new=0, autoraise=False)

#################### GUI ####################
class App(ctk.CTk):
    numResults = 0
    labels = []
    def __init__(self):
        super().__init__()

        self.labels.append(ctk.CTkLabel(master=self,
                                  font=("Arial",20),
                                  text="Results: " + str(self.numResults)))
        self.labels[0].grid(row=0,column=0,padx=20)
        self.my_frame = MyFrame(master=self, width=1000, height=400)
        self.my_frame.grid(row=1, column=0, padx=20)
        

class MyFrame(ctk.CTkScrollableFrame):

    buttons = []
    xbuttons = []

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def createBtn(self,title,url,alreadySeen=False):
        btnNum = self.numRows
        self.buttons.append(ctk.CTkButton(self,
                text=title,
                command= lambda: btnCall(self.buttons[btnNum],url),
                hover_color="green",
                font=("Arial",20),
                width=self.cget("width") - 100,
            ))
        if alreadySeen:
            self.buttons[btnNum].configure(fg_color="#5A5A5A")
        self.buttons[btnNum].grid(row=self.numRows,column=0,pady=5,padx=10)

        self.xbuttons.append(ctk.CTkButton(self,
                text="X",
                command= lambda: xBtnCall(self.buttons[btnNum]),
                hover_color="red",
                font=("Arial",20),
                width=self.cget("width") - self.buttons[0].cget("width") - 10
            ))
        self.xbuttons[btnNum].grid(row=self.numRows,column=1,pady=5)
        self.numRows += 1

    numRows = 0

class MyWordFrame(ctk.CTkScrollableFrame):

    buttons = []

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def createBtn(self,event,btnStr=None):
        btnNum = self.numRows
        self.buttons.append(ctk.CTkLabel(self,
                # text=event.widget.get(),
                font=("Arial",12),
                height=4
            ))
        self.buttons[btnNum].grid(row=self.numRows,column=0,pady=5,padx=10)
        if btnStr == None:
            self.buttons[btnNum].configure(text=event.widget.get())
        else:
            self.buttons[btnNum].configure(text=btnStr)
        self.numRows += 1

    def loadWord(self,btnStr):
        self.createBtn(None,btnStr)
    
    numRows = 0

def submitWord(event):
    file = open("words.txt","a")
    file.write("\n" + event.widget.get())
    file.close()
    wordFrame.createBtn(event)




############################ MAIN #############################

debug = False


#unwanted word filter list (case doesnt matter)
file = open("words.txt","r+")
filteredWordList = file.read().splitlines()
file.close()

#open file to store unique links"
file = open("joblinks.txt","r+")
alreadySearchedJobsList = file.read().splitlines()
file.close()



ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
window = App()
window.geometry("1080x750")

#do the job search
file = open("joblinks.txt","a")
driver = webdriver.Chrome(ChromeDriverManager().install())
populateJobs(driver,window)
file.close()

entryFrame = ctk.CTkFrame(master=window)
entryFrame.grid(row=2,column=0,padx=20)
entryFrame.place(relx=0.02,y=450)

entryWord = ctk.CTkEntry(master=entryFrame,
                     width=300,
                     font=("Arial",20),
                     placeholder_text="Enter word to filter out...",
                     )
entryWord.grid(row=0,column=0,padx=20)

wordFrame = MyWordFrame(master=entryFrame,
                                   width=200,
                                   height=200,
                                   )
wordFrame.grid(row=0,column=2,padx=20,pady=20)


for word in filteredWordList:
    wordFrame.loadWord(word)

entryWord.bind('<Return>', submitWord)

window.mainloop()






