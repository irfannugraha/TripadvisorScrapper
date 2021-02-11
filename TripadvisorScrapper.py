from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from pandas import DataFrame
from re import sub
from time import sleep

# Code by Irfan Nugraha - https://github.com/irfannugraha
# Code ini digunakan untuk melakukan scrapper di website tripadvisor.co.id
# Code ini bersifat open source

__author__    = "Irfan Nugraha"
__copyright__ = "Copyright (C) 2021 Irfan Nugraha"
__version__   = "1.0"

class methodLibrary:
  def __init__(self, link='https://www.tripadvisor.co.id'):
    try:
      options = webdriver.ChromeOptions()
      options.add_argument('--headless')
      options.add_argument('--hide-scrollbars')
      options.add_argument('--disable-gpu')
      options.add_argument("--log-level=3")

      self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
      self.driver.get(link)
    except:
      print('(!!)Eror code 100, tanya Irfan ya')
      exit()
  
  def input_element_by_xpath(self, xpath, valInpt, isTerimnate=False):
    try:
      WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable( (By.XPATH, xpath) ) )
      self.driver.find_element_by_xpath(xpath).click
      self.driver.find_element_by_xpath(xpath).send_keys(valInpt)
      return True
    except:
      if isTerimnate:
        print('(!!)Eror code 101, tanya Irfan ya')
        exit()
      else:
        return False
    
  def click_element_by_xpath(self, xpath, isTerimnate=False):
    try:
      WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable( (By.XPATH, xpath) ) )
      self.driver.find_element_by_xpath(xpath).click()
      return True
    except:
      if isTerimnate:
        print('(!!)Eror code 102, tanya Irfan ya')
        exit()
      else:
        return False

  def click_element_by_class(self, className, isTerimnate=False):
    try:
      WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable( (By.CLASS_NAME, className) ) )
      self.driver.find_element_by_class_name(className).click()
      return True
    except:
      if isTerimnate:
        print('(!!)Eror code 103, tanya Irfan ya')
        exit()
      else:
        return False

  def find_element_by_xpath(self, xpath, wait=10, isTerimnate=False):
    try:
      WebDriverWait(self.driver, wait).until(ec.element_to_be_clickable( (By.XPATH, xpath) ) )
      return True
    except:
      if isTerimnate:
        print('(!!)Eror code 104, tanya Irfan ya')
        exit()
      else:
        return False

  def install_beautifullSoup(self):
    try:
      self.soup = BeautifulSoup(self.driver.page_source, "html.parser")
    except:
      print('(!!)Eror code 105, tanya Irfan ya')
      exit()

  def export_to_bf4(self):
    try:
      soup = BeautifulSoup(self.driver.page_source, "html.parser")
      return soup
    except:
      print('(!!)Eror code 106, tanya Irfan ya')
      exit()

print('++++++++++++++++++++++++++++++++++++++++++')
print('+       tripadvisor.co.id scrapper       +')
print('+                                        +')
print('+       Copyright by Irfan Nugraha       +')
print('+     https://github.com/irfannugraha    +')
print('++++++++++++++++++++++++++++++++++++++++++')
print()
print()
link      = input('Link         : ')
jumlah    = input('Jumlah data  : ')
bahasa    = input('Bahasa       : ')
nama      = input('Nama Excel   : ')

if not link:
  print('(!!)Mohon masukan link')
  exit()
jumlah = int(jumlah) if jumlah else 0
bahasa = bahasa if bahasa else 'Indonesia'
nama = nama if nama else 'hasil'
data = {}

web = methodLibrary(link)
link = sub("https://www\.tripadvisor\.co\.id/|_Review.*", '', link)

print()
if( (web.find_element_by_xpath('//span[contains(@class, "ui_icon thumbs-up")]', 10)) ):
  print('Scrapping mulai', end='\r')
  jumlah = jumlah if jumlah > 0 else float('inf')
  idx = 1
  sleep(10)
  if (link == 'Attraction'):
      
      if( web.click_element_by_xpath('//span[text(), "'+bahasa+'"]') ):
        pass
      elif( web.click_element_by_xpath('//div[contains(@class, "_21ggebu7")]/span') ):
        if ( web.click_element_by_xpath('//div[contains(@class, "_32oTjHgM")]//label[contains(text(), "'+bahasa+'")]') ):
          pass
        else:
          print('(!!)Bahasa tidak ditemukan')
          exit()
      else:
        print('(!!)Bahasa tidak ditemukan')
        exit()

      data = { 'nama' : [], 'Bulan Ulasan' : [], 'rating' : [], 'judul' : [], 'ulasan' : [], 'Tgl Pengalaman' : [], 'jenisTrip' : []}
      while idx<jumlah:
        web.click_element_by_xpath('//span[contains(text(), "Selengkapnya")]')
        sleep(10)
        soup = web.export_to_bf4()

        # get ulasan
        reviewTag = soup.findAll(attrs={"class":"Dq9MAugU"})
        for item in reviewTag:
          print('Scrapping ulasan ke '+str(idx), end='\r')
          data['nama'].append(            item.find(attrs={"class":"ui_header_link"}).get_text() )
          data['Bulan Ulasan'].append(       sub('<div.*menulis ulasan |</span.*>', '', str(item.find(attrs={"class":"_2fxQ4TOx"})) ) )
          data['rating'].append(          sub('<div.*bubble_|0">.*', '', str(item.find(attrs={"class":"nf9vGX55"})) ) )
          data['judul'].append(           sub('<div.*<span>|</span>.*','', str(item.find(attrs={"data-test-target":"review-title"})) ) )
          data['ulasan'].append(          sub( '<[^>]*>', '', str(item.find(attrs={"class":"IRsGHoPm"})) ) )
          data['Tgl Pengalaman'].append(   sub( '^<span.*:</span> |</span>', '', str(item.find(attrs={"class":"_34Xs-BQm"})) ) )
          data['jenisTrip'].append(       sub( '^<span.*: </span>|</span>', '', str(item.find(attrs={"class":"_2bVY3aT5"})) ) )
          idx+=1
          if idx>=jumlah:
            break
        
        if (web.find_element_by_xpath('//a[contains(@class, "ui_button nav next primary ")]') and (idx<jumlah)):
          web.click_element_by_xpath('//a[contains(@class, "ui_button nav next primary ")]')
        else:
          break

        sleep(5)  
  elif(link == 'Hotel'):

      if( web.click_element_by_xpath('//label[@for="LanguageFilter_2"]//span[contains(text(), "'+bahasa+'")]') ):
        pass
      elif( web.click_element_by_xpath('//div[contains(@class, "_21ggebu7")]/span') ):
        if ( web.click_element_by_xpath('//div[contains(@class, "_32oTjHgM")]//label[contains(text(), "'+bahasa+'")]') ):
          pass
        else:
          print('(!!)Bahasa tidak ditemukan')
          exit()
      else:
        print('(!!)Bahasa tidak ditemukan')
        exit()    

      data = {'nama':[],'Bulan Ulasan':[],'rating':[],'judul':[],'ulasan':[],'Tgl Pengalaman':[],'jenisTrip':[],}
      while idx<jumlah:
        web.click_element_by_xpath('//div[contains(@data-test-target, "expand-review")]//span[contains(text(), "Selengkapnya")]')
        sleep(10)
        soup = web.export_to_bf4()

        # get ulasan
        reviewTag = soup.findAll(attrs={"data-test-target":"HR_CC_CARD"})
        for item in reviewTag:
          print('Scrapping ulasan ke '+str(idx), end='\r')
          data['nama'].append(          item.find(attrs={"class":"ui_header_link"}).get_text() )
          data['Bulan Ulasan'].append(     sub('<div.*menulis ulasan |</span.*>', '', str(item.find(attrs={"class":"_2fxQ4TOx"})) ) )
          data['rating'].append(        sub('<div.*bubble_|0">.*', '', str(item.find(attrs={"class":"nf9vGX55"})) ) )
          data['judul'].append(         sub('<div.*<span>|</span>.*','', str(item.find(attrs={"data-test-target":"review-title"})) ) )
          data['ulasan'].append(        sub( '<[^>]*>', '', str(item.find(attrs={"class":"IRsGHoPm"})) ) )
          data['Tgl Pengalaman'].append( sub( '^<span.*:</span> |</span>', '', str(item.find(attrs={"class":"_34Xs-BQm"})) ) )
          data['jenisTrip'].append(     sub( '<[^>]*>|Jenis Trip: ', '', str(item.find(attrs={"class":"_2bVY3aT5"})) ) )
          idx+=1
          if idx>=jumlah:
            break
        
        if (web.find_element_by_xpath('//a[contains(@class, "ui_button nav next primary ")]') and (idx<jumlah)):
          web.click_element_by_xpath('//a[contains(@class, "ui_button nav next primary ")]')
        else:
          break

        sleep(5)
  elif(link == 'Restaurant'):

      if( web.click_element_by_xpath('//span[text(), "'+bahasa+'"]') ):
        pass
      elif( web.click_element_by_xpath('//div[@class="taLnk"]/span') ):
        if ( web.click_element_by_xpath('//div[contains(@class, "more-options")]//label[contains(text(), "'+bahasa+'")]') ):
          pass
        else:
          print('(!!)Bahasa tidak ditemukan')
          exit()
      else:
        print('(!!)Bahasa tidak ditemukan')
        exit()

      data = {'nama':[],'Bulan Ulasan':[],'rating':[],'judul':[],'ulasan':[],'Tgl Pengalaman':[]}
      while idx<jumlah:
        web.click_element_by_xpath('//span[contains(text(), "Selengkapnya")]')
        sleep(10)
        soup = web.export_to_bf4()

        # get ulasan
        lastReviewTag = soup.find(attrs={"id":"REVIEWS"}).find(attrs={"class":"listContainer hide-more-mobile"}).find_all(attrs={"class":"info hidden"})
        i =0;
        reviewTag = []
        for item in lastReviewTag:
          reviewTag.append(item.find_parent('div'))
          # print(reviewTag[i])
          i+=1

        for item in reviewTag:
          print('Scrapping ulasan ke '+str(idx), end='\r')
          data['nama'].append(   sub( '^<div.*<div>|</div></div>', '', str(item.find(attrs={"class":"info_text pointer_cursor"})) ) )
          data['Bulan Ulasan'].append(  sub( '^<span.*Diulas pada |</span.*>', '', str(item.find(attrs={"class":"ratingDate"})) ) )
          data['rating'].append(   sub( '^<span.*bubble_|0">.*', '', str(item.find(attrs={"class":"ui_bubble_rating"})) ) )
          data['judul'].append(  sub( '^<span.*">|</span>.*', '', str(item.find(attrs={"data-test-target":"noQuotes"})) ) )
          data['ulasan'].append(   sub( '<[^>]*>', '', sub( '^<div.*partial_entry">|</p>.*', '', str(item.find(attrs={"class":"prw_rup prw_reviews_text_summary_hsx"})) ) ) )
          data['Tgl Pengalaman'].append(  sub( '^<div.*:</span> |</div>', '', str(item.find(attrs={"class":"prw_rup prw_reviews_stay_date_hsx"})) ) )
          idx+=1
          if idx>=jumlah:
            break

        sleep(5)
        if (web.find_element_by_xpath('//div[@id="REVIEWS"]//a[contains(@class, "nav next ui_button primary")]') and (idx<jumlah)):
          print('still got it bois')
          web.click_element_by_xpath('//div[@id="REVIEWS"]//a[contains(@class, "nav next ui_button primary")]')
        else:
          break

        sleep(5)
  elif(link == 'Airline'):
      if( web.click_element_by_xpath('//span[text(), "'+bahasa+'"]') ):
        pass
      elif( web.click_element_by_xpath('//div[contains(@class, "_21ggebu7")]/span') ):
        if ( web.click_element_by_xpath('//div[contains(@class, "_32oTjHgM")]//label[contains(text(), "'+bahasa+'")]') ):
          pass
        else:
          print('(!!)Bahasa tidak ditemukan')
          exit()
      else:
        print('(!!)Bahasa tidak ditemukan')
        exit()  

      data = { 'nama':[],'Bulan Ulasan':[],'rating':[],'judul':[],'ulasan':[],'Tgl Pengalaman':[],'jenisTrip':[]}
      while idx<jumlah:
        web.click_element_by_xpath('//span[text(), "Selengkapnya"]')
        sleep(10)
        soup = web.export_to_bf4()

        # get ulasan
        reviewTag = soup.find(attrs={"class":"_7PJap-I0 _3-JlUfTE"}).next_sibling()[0].findAll(attrs={"class":"Dq9MAugU T870kzTX LnVzGwUB"}, recrusive=False)
        for item in reviewTag:
          print('Scrapping ulasan ke '+str(idx), end='\r')
          data['nama'].append(  item.find(attrs={"class":"ui_header_link"}).get_text() )
          data['Bulan Ulasan'].append( sub('<div.*menulis ulasan |</span.*>', '', str(item.find(attrs={"class":"_2fxQ4TOx"})) ) )
          data['rating'].append(  sub('<div.*bubble_|0">.*', '', str(item.find(attrs={"class":"nf9vGX55"})) ) )
          data['judul'].append( sub('<div.*<span>|</span>.*','', str(item.find(attrs={"data-test-target":"review-title"})) ) )
          data['ulasan'].append(  sub( '<[^>]*>', '', str(item.find(attrs={"class":"IRsGHoPm"})) ) )
          data['Tgl Pengalaman'].append( sub( '^<span.*:</span> |</span>', '', str(item.find(attrs={"class":"_34Xs-BQm"})) ) )
          data['jenisTrip'].append( item.find(attrs={"class":'_3tp-5a1G'}).get_text() )
          idx+=1
          if idx>=jumlah:
            break
        
        if (web.find_element_by_xpath('//a[contains(@class, "ui_button nav next primary ")]') and (idx<jumlah)):
          web.click_element_by_xpath('//a[contains(@class, "ui_button nav next primary ")]')
        else:
          break

        sleep(5)
  else:
    print('(!!)Link yang dimasukan salah')
    exit()
else:
  print('(!!)Ulasan kosong')
  exit()

print('Scrapping selesai                                                                      ')


print('Membuat Excel...', end='\r')

isExcelError = True
while (isExcelError == True):
  isExcelError = False
  try:
    df = DataFrame(data)
    df.to_excel(('/'+nama+'.xlsx'), index=True, header=True)
  except:
    print('(!!)Terjadi Error, coba tutup file excel "hasil.xlsx" lalu enter', end='\r')
    input()
    isExcelError = True

print('Membuat Excel selesai                                                                       ')

print('Hasil disimpan pada "[Lokasi Aplikasi]/HasilScrap/'+nama+'.xlsx"                            ')