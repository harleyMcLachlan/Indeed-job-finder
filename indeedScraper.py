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

### Main function to populate screen with jobs
def populateJobs(driver,window):

    #OPENS indeed to engineer jobs in berlin last 24 hours
    driver.get("https://de.indeed.com/jobs?q=engineer&l=Berlin&fromage=1&vjk=0a4a7664e5720982")

    #Loops through each page
    while True:
        getJobs(driver,window)
        if(debug or not(nextPage(driver))):                                                 #Break if debug mode is on or run out of pages
            time.sleep(0.5)                                                                 #Give time to load last page. (Crashes without)
            window.labels[0].configure(text="Results: " + str(window.my_frame.numRows))     #Update the results text
            driver.close()                                                                  #Close the chrome window
            break

###Get list of jobs on page            
def getJobs(driver,window):
    closePopups(driver)
    jobList = driver.find_elements(By.XPATH,"/html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul/li")    #Gets all jobs elements on page
    
    for jobListing in jobList:                                                                                      #For each job, get snippet text
        snippet = jobListing.find_elements(By.CLASS_NAME,"job-snippet")                                                                                                       #For each snippet detect the language
        try:                                                                                                    
            if detect(snippet[0].text) == "en":                                                                     #Check language of snippet
                titleElement = jobListing.find_elements(By.CLASS_NAME,"jobTitle")                                   #Get job title element
                checkTitle(titleElement[0],jobListing,window,file)                                                  #check title for filtered words and already seen jobs
        except:
            pass

### check title for filtered words and already seen jobs
def checkTitle(titleElement,jobListing,window,jobFile):
    jobTitle = trimMaxStrLen(titleElement.text) #shorten job title if needed

    #check title for filtered words (makes everything lowercase for comparison)
    if any(filteredWord.lower() in titleElement.text.lower() for filteredWord in filteredWordList):
        return
    
    jobLinkElement = jobListing.find_elements(By.CLASS_NAME,"jcs-JobTitle")                                 #Get job link element
    
    #check titles for already seen jobs
    if any(alreadyOpenedJobTitles in jobTitle for alreadyOpenedJobTitles in alreadySeenJobsList):
        window.my_frame.createBtn(jobTitle,jobLinkElement[0].get_attribute('href'),True)                    #If already seen, create greyed button
    else:
        window.my_frame.createBtn(jobTitle,jobLinkElement[0].get_attribute('href'))                         #If not seen, create blue button
        jobFile.write(jobTitle + "\n")                                                                      #and write title to the seen jobs list
    
### goes to next page of jobs if possible
def nextPage(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")                                #Scroll to bottom of page                            
    time.sleep(0.2)                                                                                         #Wait for scroll to complete
    page = driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Next Page']")                                #Get next page element
    if len(page) == 0:                                                                                      #Return false if no more next page
        return 0
    try:
        page[0].click()                                                                                     #Otherwise click next page
    except:
        time.sleep(0.5)                                                                                     #Sometimes need to wait for popups and try again
        closePopups(driver)
        page[0].click()

    elem=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"job-snippet")))       #Wait for next page to load
    return 1

########################## HELPER FUNCTIONS ############################

### Checks for and closes popups
def closePopups(driver):
    #Store all elements with close buttons in array
    closeButtonElements = []
    try:
        closeButtonElements.append(driver.find_elements(By.CLASS_NAME,"icl-CloseButton"))
    except:

        pass
    try:
        closeButtonElements.append(driver.find_elements(By.ID,"onetrust-reject-all-handler"))
    except:
        pass

    try:
        closeButtonElements.append(driver.find_elements(By.CSS_SELECTOR,"button[aria-label='schließen']"))
    except:
        pass

    try:
        closeButtonElements.append(driver.find_elements(By.CSS_SELECTOR,"button[aria-label='close']"))
    except:
        pass

    #Click on all the close buttons
    for closeButtonElement in closeButtonElements:
        for closeButton in closeButtonElement:
            try:
                closeButton.click()
            except:
                pass

### Trim length of job title to fit in window
def trimMaxStrLen(str,len=70):
    return str[:len]

### opens link in default browser
def openLink(url):
    webbrowser.open(url, new=0, autoraise=False)

### Opens job link
def jobBtnCall_openJobLink(btn,url):
    openLink(url)
    btn.configure(fg_color="grey")

### Deletes job from GUI list
def XBtnCall_deleteJob(btn):
    btn.configure(fg_color="transparent")

### Submits word to filtered word list
def entryCall_submitWord(event):
    file = open("filtered words.txt","a")
    file.write("\n" + event.widget.get())
    file.close()
    wordFrame.createBtn(event)

########################## GUI ############################
class App(ctk.CTk):
    numResults = 0
    labels = []
    def __init__(self):
        super().__init__()
        self.labels.append(ctk.CTkLabel(master=self, font=("Arial",20), text="Results: " + str(self.numResults)))
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
                command= lambda: jobBtnCall_openJobLink(self.buttons[btnNum],url),
                hover_color="green",
                font=("Arial",20),
                width=self.cget("width") - 100,
            ))
        self.buttons[btnNum].grid(row=self.numRows,column=0,pady=5,padx=10)
        if alreadySeen:
            self.buttons[btnNum].configure(fg_color="#5A5A5A")

        self.xbuttons.append(ctk.CTkButton(self,
                text="X",
                command= lambda: XBtnCall_deleteJob(self.buttons[btnNum]),
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

### setup main window and wigdets
def windowSetup():
    #set main window properties
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    window.geometry("1080x750")

    #setup frame to hold word filter related widgets
    entryFrame = ctk.CTkFrame(master=window)
    entryFrame.grid(row=2,column=0,padx=20)
    entryFrame.place(relx=0.02,y=450)

    #setup entry box for filter words
    entryWord = ctk.CTkEntry(master=entryFrame,
                        width=300,
                        font=("Arial",20),
                        placeholder_text="Enter word to filter out...",
                        )
    entryWord.grid(row=0,column=0,padx=20)
    entryWord.bind('<Return>', entryCall_submitWord)

    #setup frame to hold filter words
    wordFrame = MyWordFrame(master=entryFrame,
                                    width=200,
                                    height=200,
                                    )
    wordFrame.grid(row=0,column=2,padx=20,pady=20)

    #load words into the filtered word window
    for word in filteredWordList:
        wordFrame.loadWord(word)

############################ MAIN #############################
if __name__ == "__main__":
    debug = False

    #get unwanted word filter list (case doesnt matter)
    file = open("filtered words.txt","r+")
    filteredWordList = file.read().splitlines()
    file.close()

    #open file to read unique already seen job titles"
    file = open("seen jobs.txt","r+")
    alreadySeenJobsList = file.read().splitlines()
    file.close()
    
    window = App()
    windowSetup()

    #do the job search
    file = open("seen jobs.txt","a")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    populateJobs(driver,window)
    file.close()
    window.mainloop()






