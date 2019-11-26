from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
from selenium.webdriver.firefox.options import Options

global driver
driver = ""

def get_source(srcStn, srcCity, destStn, destCity, dd, mm, yyyy):

    srcStn = srcStn.strip()
    srcCity = srcCity.strip()
    srcCity = srcCity.replace(' ', '&')
    destStn = destStn.strip()
    destCity = destCity.strip()
    destCity = destCity.replace(' ', '&')

    url = 'https://railways.makemytrip.com/listing?date=' + str(yyyy) + str(mm) + str(dd)
                + '&srcStn=' + srcStn + '&srcCity=' + srcCity + '&destStn=' + destStn + '&destCity=' + destCity + '&classCode='

    options = Options()
    options.headless = True
    driver = wd.Firefox(options=options)

    driver.get(url)
    source_code = driver.page_source
    time.sleep(0.5)
    driver.close()
    # print(source_code)
    modSource = ""
    try:
        for i in source_code:
            modSource = modSource + i
    except:
        bool = 0

    raw = ""

    for i in modSource:
        try:
            # print(i, end="")
            if(i!='\u20b9' and i!='\ufffd'):
                raw = raw + i
        except:
            continue

    return(raw)

def gettraindata(rawData):

    soup = BeautifulSoup(rawData, 'html5lib')

    # print(soup.prettify())

    traindata = []

    for row1 in soup.findAll('div', attrs = {'class':'railInfo railTitle'}):

        train = []
        #
        # for row in row1.findAll('p', attrs = {'class':'appendBottom10 latoBlack font22 blackText'}):
        #     train.append(row.text[1:])


        temp = row1.text

        hl = temp.find('#')
        tr = temp[1:hl-2]
        # print(tr)

        temp = temp[hl:]
        hl = temp.find('D')
        trainno = temp[:hl-1]
        # print(trainno)

        departs = ""

        for row in row1.findAll('span', attrs = {'class':'greenText latoBold'}):
            departs = departs + " " + (row.text)
        departs = departs.strip()
        # print(departs)

        train.append(tr)
        train.append(trainno)
        train.append(departs)

        traindata.append(train)

    # print()

    # for row1 in soup.findAll('span', attrs = {'class':'font22 latoBold'}):
    #     print(row1.text)
    #     # print()
    #
    # print()
    i = 0
    for row1 in soup.findAll('div', attrs = {'class':'railInfo railDeparture'}):
        tt = row1.text
        tp = tt.find('M')
        # print(tt[1:tp+1], end=" ")
        # print(tt[tp+4:tp+8])
        # print(tt[tp+8:])
        # print()

        at = tt[1:tp+1] + " " + tt[tp+4:tp+8]
        att = tt[tp+8:]
        traindata[i].append(at)
        traindata[i].append(att)
        i = i+1

    # print()

    i = 0
    for row1 in soup.findAll('div', attrs = {'class':'railInfo textCenter railDuration'}):
        tt = row1.text
        dr = tt[:tt.find('V')-1]
        # print(dr)
        traindata[i].append(dr)
        i = i+1


    # print()

    i = 0
    for row1 in soup.findAll('div', attrs = {'class':'railInfo railArrival'}):
        tt = row1.text
        tp = tt.find('M')
        # print(tt[1:tp+1], end=" ")
        # print(tt[tp+4:tp+8])
        # print(tt[tp+8:])
        # print()

        dt = tt[1:tp+1] + " " + tt[tp+4:tp+8]
        dtt = tt[tp+8:]
        traindata[i].append(dt)
        traindata[i].append(dtt)
        i = i+1
    # print()

    i = 0
    for row1 in soup.findAll('div', attrs = {'class':'railClassBox'}):
        allclasses = []
        classes = []
        tt = row1.text
        ti = 0
        tp = tt.find('ago')
        while(tp!=-1):
            # tclass = []
            allclasses.append(tt[ti:tp+3])
            ti = tp+3
            tp = tt.find('ago', ti)
            # classes.append(tclass)
        for j in allclasses:
            ttt = []
            tp = 0
            if j.find('Click to update')!=-1:
                j = j[j.find('Click to update')+14:]
            if j.find('AC Chair Car')!=-1:
                ttt.append('AC Chair Car')
                tp = len('AC Chair Car')
            elif j.find('Executive Chair Car')!=-1:
                ttt.append('Executive Chair Car')
                tp = len('Executive Chair Car')
            elif j.find('3 Tier AC')!=-1:
                ttt.append('3 Tier AC')
                tp = len('3 Tier AC')
            elif j.find('2 Tier AC')!=-1:
                ttt.append('2 Tier AC')
                tp = len('2 Tier AC')
            elif j.find('1st Class AC')!=-1:
                ttt.append('1st Class AC')
                tp = len('1st Class AC')
            elif j.find('Executive Anubhuti')!=-1:
                ttt.append('Executive Anubhuti')
                tp = len('Executive Anubhuti')
            elif j.find('Sleeper')!=-1:
                ttt.append('Sleeper')
                tp = len('Sleeper')
            elif j.find('Second Sitting')!=-1:
                ttt.append('Second Sitting')
                tp = len('Second Sitting')
            # elif j.find('')!=-1:
            #     ttt.append('')
            #     tp = len('')
            # elif j.find('')!=-1:
            #     ttt.append('')
            #     tp = len('')
            else:
                print(j)
                continue

            fare = ""

            for k in j[tp:]:
                if k.isdigit():
                    fare = fare + k
                    tp = tp + 1
                else:
                    break
            ttt.append(fare)

            up = j[tp:].find('Updated')

            ttt.append(j[tp:tp+up])
            ttt.append(j[tp+up:])

            classes.append(ttt)
            # print(ttt)
            # print(j[tp:])
        # print(classes)
        # print()
        traindata[i].append(classes)
        i = i+1

def train

def test():

    get_source(srcStn, srcCity, destStn, destCity, dd, mm, yyyy):

    for i in traindata:
        for j in i:
            print(j)
        print()