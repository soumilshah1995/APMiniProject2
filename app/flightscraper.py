from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as OptionsCr
import json
from app.OSDetect import osDetect



global driver
driver = ""


def flightData(rawData):
    soup = BeautifulSoup(rawData, 'html5lib')
    # xxx= soup.prettify()
    # for i in xxx:
    #     print(i, end="")
    flights = [] # Departure City, Arrival City, Airline, Flight No, Departure Time, Arrival Time, Flight Duration,, No of stops

    for row1 in soup.findAll('div', attrs = {'class':'schedule v-aligm-t pr'}):

        flight = []

        t1 = row1.findAll('div', attrs = {'class':'i-b pr'})
        for row in t1:
            dt = str(row)
            dt = dt[20:25]

            ar = str(row.p)
            ar = ar[71:]
            ar = ar[:ar.find('<')]

            fn = row.span.text


        t2 = row1.findAll('p', attrs = {'class':'fs-10 font-lightgrey no-wrap city ellipsis'})
        for row in t2:
            flight.append(row.text)

        t3 = row1.findAll('p', attrs = {'autom':'arrivalTimeLabel'})
        for row in t3:
            at = str(row.text)

        t4 = row1.findAll('p', attrs = {'autom':'durationLabel'})
        for row in t4:
            dr = row.text

        t5 = row1.findAll('span', attrs = {'class':'cursor-default'})
        for row in t5:
            st = row.text

        flight.append(ar)
        flight.append(fn)
        flight.append(dt)
        flight.append(at)
        flight.append(dr)
        n = fn.count('/')
        if n==0:
            flight.append(st)
        else:
            flight.append(str(n) + " Stop(s)")
        flights.append(flight)

    # print(flights)

    return(flights)


def get_source(departureCode, arrivalCode, dd, mm, yyyy):

    syst = osDetect()

    if syst=='W':
        options = Options()
        options.headless = True
        # path = os.path.dirname(os.path.realpath(__file__))
        # +"\\drivers\\Windows\\geckodriver"
        driver = wd.Firefox(executable_path = r'drivers\Windows\geckodriver.exe', options=options)
    elif syst=='M':

        # options = Options()
        # options.headless = True
        # driver = wd.Firefox(executable_path = r'drivers/MacOS/geckodriver', options=options)
        # driver = wd.Firefox(executable_path = r'//usr/local/bin/geckodriver', options=options)

        # options = wd.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument("--test-type")
        # options.binary_location = "/usr/bin/chromium"
        # driver = wd.Chrome(chrome_options=options)

        # chrome_options = wd.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # driver = wd.Chrome(options = chrome_options)


        # options = wd.ChromeOptions()
        # options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        # options.add_argument('headless')
        # driver = wd.Chrome(chrome_options=options)

        driver = wd.Chrome()

        # chrome_options = OptionsCr()
        # chrome_options.add_argument("--headless")
        # driver = wd.Chrome('chromedriver')
        # driver = wd.Chrome(executable_path='//Users/raj.burad7/Desktop/APMiniProject2/app/chromedriver',options=chrome_options)
        # driver = wd.Chrome(options=chrome_options)
        # driver = wd.Chrome(executable_path='drivers/MacOS/geckodriver',options=chrome_options)
        # driver = wd.Chrome(executable_path='drivers/MacOS/geckodriver')

        # Other Code

        # # chrome_options = wd.ChromeOptions()
        # chrome_options = OptionsCr()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors.
        # driver = wd.Chrome(executable_path='drivers/MacOS/geckodriver', chrome_options=chrome_options)

    elif syst=='L':
        #Linux Code
        options = Options()
        options.headless = True
        driver = wd.Firefox(executable_path = r'drivers/Linux/geckodriver', options=options)

    url = 'https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=' + str(departureCode)+ '&originCountry=IN&destination=' + str(arrivalCode) + '&destinationCountry=IN&flight_depart_date='+str(dd)+'%2F'+str(mm)+'%2F'+str(yyyy)+'&ADT=1&CHD=0&INF=0&class=Economy&source=fresco-home&version=1.8'
    driver.get(url)
    source_code = driver.page_source
    time.sleep(0.5)
    driver.close()
    modSource = ""
    try:
        for i in source_code:
            modSource = modSource + i
    except:
        bool = 0
    return(modSource)

def jsonData(rawData):
    soup = BeautifulSoup(rawData, 'html5lib')
    i = 1
    yy = ""
    for row1 in soup.findAll('script', attrs = {'type':'text/javascript'}):
        if i!=10:
            i = i+1
            continue
        # print(row1.prettify())
        yy = str(row1.text)
        break
    # val = -1
    # for i in range(0, 4):
    #     val = yy.find(';', val + 1)
    val = yy.find('mainData')
    val = yy.find('mainData', val+1)
    yy = yy[yy.find('{'):val-10]
    return(yy)


def flightFares(rawJSON, flights, departureCode, arrivalCode, dd, mm, yyyy):

    ff = []
    # soup = BeautifulSoup(rawData, 'html5lib')
    # # qqq = soup.prettify()
    # # try:
    # #     for i in qqq:
    # #         print(i,end="")
    # # except:
    # #     bool = 0
    #
    # # print(soup.prettify())
    # # print()
    # # print()
    # i = 1
    # yy = ""
    # for row1 in soup.findAll('script', attrs = {'type':'text/javascript'}):
    #     if i!=10:
    #         i = i+1
    #         continue
    #     # print(row1.prettify())
    #     yy = str(row1.text)
    #     break
    # # val = -1
    # # for i in range(0, 4):
    # #     val = yy.find(';', val + 1)
    # val = yy.find('mainData')
    # val = yy.find('mainData', val+1)
    # yy = yy[yy.find('{'):val-10]

    print(rawJSON)
    y = json.loads(rawJSON)

    # for i in range(len(flights)):
    #
    #      # print(y["resultData"][-1]["fareDetails"]["DELBOM20191128"][we]["O"]["ADT"]["tf"])
    #      # lc = ""
    #      # if flights[i][2]=='IndiGo':
    #      #     lc = "6EAPI"
    #      # elif flights[i][2]=='Go Air':
    #      #     lc = "G8API"
    #      # elif flights[i][2]=='Air India':
    #      #     lc = "GALDOM"
    #      # elif flights[i][2]=='SpiceJet':
    #      #     lc = "SGAPI"
    #      # elif flights[i][2]=='Vistara':
    #      #     lc = "1AWS4"
    #      # elif flights[i][2]=='Air Asia':
    #      #     lc = "AASAPIDOM"
    #      # fl = flights[i][3].replace('-', '')
    #
    #      dtdt = str(yyyy) + str(mm) + str(dd)
    #      # we = departureCode + arrivalCode + fl + dtdt + "_" + lc
    #      ae =  departureCode + arrivalCode + dtdt
    #      # for j in y["resultData"]:
    #      #     print(j["fareDetails"]["DELBOM20191128"])
    #      for j in y["resultData"]:
    #          try:
    #              # print(j["fareDetails"][ae][we]["O"]["ADT"]["tf"])
    #              # print(j["fareDetails"][ae])
    #
    #              for k in j["fareDetails"][ae]:
    #
    #                 zzz = str(k)
    #                 print(j["fareDetails"][ae][zzz]["O"]["ADT"]["tf"])
    #
    #              # flights[i].append(j["fareDetails"][ae][we]["O"]["ADT"]["tf"])
    #              # break
    #
    #          except:
    #              continue
    #      break


    for i in range(len(flights)):

         # print(y["resultData"][-1]["fareDetails"]["DELBOM20191128"][we]["O"]["ADT"]["tf"])
         lc = ""
         if flights[i][2]=='IndiGo':
             lc = "6EAPI"
         elif flights[i][2]=='Go Air':
             lc = "G8API"
         elif flights[i][2]=='Air India':
             lc = "GALDOM"
         elif flights[i][2]=='SpiceJet':
             lc = "SGAPI"
         elif flights[i][2]=='Vistara':
             lc = "1AWS4"
         elif flights[i][2]=='Air Asia':
             lc = "AASAPIDOM"
         fl = flights[i][3].replace('-', '')

         dtdt = str(yyyy) + str(mm) + str(dd)
         we = departureCode + arrivalCode + fl + dtdt + "_" + lc
         ae =  departureCode + arrivalCode + dtdt
         # for j in y["resultData"]:
         #     print(j["fareDetails"]["DELBOM20191128"])
         bool = False
         for j in y["resultData"]:
             try:
                 # print(j["fareDetails"][ae][we]["O"]["ADT"]["tf"])
                 # print(ae)
                 # print(j["fareDetails"][ae])

                 # for k in j["fareDetails"][ae]:
                 #
                 #    zzz = str(k)
                    # print(j["fareDetails"][ae][zzz]["O"]["ADT"]["tf"])

                 flights[i].append(j["fareDetails"][ae][we]["O"]["ADT"]["tf"]) #Total Fare
                 flights[i].append(j["fareDetails"][ae][we]["O"]["ADT"]["bf"]) #Base Fare
                 flights[i].append(j["fareDetails"][ae][we]["O"]["ADT"]["YQ"]) #Fuel Surcharge
                 flights[i].append(j["fareDetails"][ae][we]["O"]["ADT"]["PSF"]) #Passenger Service Fee
                 flights[i].append(j["fareDetails"][ae][we]["O"]["ADT"]["TF"]) #CUTE Fee
                 flights[i].append(we)
                 # PSF":"Passenger Service Fee"
                 # "YQ":"Fuel Surcharge"
                 # "KKC":"Krishi Kalyan Cess"
                 # "GST":"Goods And Service Tax"
                 # "OT":"Fee And Taxes"
                 # "UDF":"User Development Fee"
                 # "JN":"Govt. Service Tax"
                 # "WC":"Airport Arrival Tax"
                 # "DF":"Development Fee"
                 # "OC":"Other Charges"
                 # "CM":"Commission"
                 # "PHF":"Add to Base"
                 # "SBC":"Swachh Bharat Cess"
                 # "TF":"CUTE Fee"
                 # "OC":"Miscelleneous"

                 bool = True

                 # break

             except:
                 continue
         # break
         if(fl[0:2]=='9I'):
              fl = 'AI' + fl[2:]
         if bool==False:
             try:
                 if flights[i][7]=='1 Stop(s)':
                     boolff = False
                     for j in y["resultData"]:
                         s = str(j["fareDetails"][ae])
                         f1n = fl.find('/')
                         fp1 = s.find(fl[:f1n])
                         # print(fl[:f1n])

                         while(fp1!=-1):
                             # print(fl[:2]+fl[f1n+1:])
                             fp2 = s.find(fl[:2]+fl[f1n+1:], fp1)

                             while(fp2!=-1):
                                 if(fp2-fp1>16 and fp2-fp1<22):
                                     # print("T1")
                                     ap = s.find(lc, fp2)
                                     if(ap-fp2>8 and ap-fp2<20):
                                         # print("T2")
                                         tflp = s.find("tf", ap)
                                         if(tflp-ap>28 and tflp-ap<42):
                                             sff = s[tflp+6:s.find(',',tflp+6)-1]
                                             # print(s[fp1:ap])
                                             flights[i].append(sff)
                                             # print(sff)
                                             boolff = True
                                             break

                                 fp2 =  s.find(fl[:2]+fl[f1n+1:], fp2+1)
                                 if(fp2-fp1>22):
                                     break
                             if(boolff==True):
                                 break
                             fp1 = s.find(fl[:f1n], fp1+1)
                         if(boolff==True):
                             break
             except:
                    print('Exception')
         else:
             bool = False

    return(flights, ae)
     # ["DELBOM6E17120191128_6EAPI"]["O"]["ADT"]["tf"])


def flightDetails(rawJSON, flights, ae):
    y = json.loads(rawJSON)
    f =[]
    for i in y["resultData"]:
        # print(i["fltSchedule"]["DELRPR20191130"])
        # print(i["fltSchedule"]["airportNames"])
        # print(i["fltSchedule"]["cityNames"])
        for j in i["fltSchedule"][ae]:
            ff = []
            ff.append(j["ID"])
            # print(j["ID"])
            # print(j["convFee"])
            for k in j["OD"]:
                ff.append(k["bga"])
                # print(k["bga"])
                # print(k["FS"])
                for l in k["FS"]:
                    fff = []
                    try:
                        fff.append(l["dac"])
                        print(l["dac"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["aac"])
                        print(l["aac"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["ddt"])
                        print(l["ddt"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["adt"])
                        print(l["adt"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["dd"])
                        print(l["dd"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["ad"])
                        print(l["ad"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["eq"])
                        print(l["eq"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["bga"])
                        print(l["bga"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["dt"])
                        print(l["dt"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["at"])
                        print(l["at"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["classtype"])
                        print(l["classtype"])
                    except:
                        fff.append("NA")
                        print("NA")
                    try:
                        fff.append(l["ml"])
                        print(l["ml"])
                    except:
                        fff.append("NA")
                        print("NA")
                ff.append(fff)
            f.append(ff)
            print()
    for i in f:
        for j in flights:
            if j[14]==i[0]:
                for k in i:
                    if k==i[0]:
                        continue
                    j.append(k)
                break
    return(flights)


def flightSearch(departureCode, arrivalCode, dd, mm, yyyy):

    source = get_source(departureCode, arrivalCode, dd, mm, yyyy)
    flights = flightData(source)
    rawJSON = jsonData(source)
    flights, ae = flightFares(rawJSON, flights, departureCode, arrivalCode, dd, mm, yyyy)


    boolExp = True
    for i in flights:
        if len(i)==9:
            boolExp = False
            break
    if boolExp==True:
        flights = flightFares(source, flights, departureCode, arrivalCode, dd, mm, yyyy)
    max = 0
    for i in range(0, len(flights)):
        flights[i].insert(0, i)
        if(max<len(flights[i])):
            max = len(flights[i])
    # print(max)
    for i in flights:
        if len(i)<max:
            for j in range(max-len(i)):
                i.append("NA")

    flights = flightDetails(rawJSON, flights, ae)

    return(flights)

def testCase():
    departureCode = "DEL"
    arrivalCode = "CCU"
    dd = 30
    mm = 11
    yyyy = 2019
    flights = flightSearch(departureCode, arrivalCode, dd, mm, yyyy)
    # print(flights)

    for i in flights:
        print(i)

# from OSDetect import osDetect
# testCase()
