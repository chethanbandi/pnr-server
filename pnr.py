from lxml import html
import httplib, urllib

from constants import *
from responsecodes import *

class PNRClass:
   pnr = {}

   def __init__(self):
      self.pnr = {}
      self.pnr["Status"] = {
                            "code": RESPONSE_CODE_SUCCESS,
                            "message": RESPONSE_MESSAGE_SUCCESS
                           }

   def getJourneyDetails(self, data):
      trElements = data.getchildren()
       
      journeyDetails = trElements[2].getchildren()
      self.pnr["TrainNumber"] = journeyDetails[0].text
      self.pnr["TrainName"]   = (journeyDetails[1].text).lstrip().rstrip()
      self.pnr["BoardingDate"] = journeyDetails[2].text
      self.pnr["From"] = journeyDetails[3].text
      self.pnr["To"] = journeyDetails[4].text
      self.pnr["ReservedUpto"] = journeyDetails[5].text
      self.pnr["BoardingPoint"] = journeyDetails[6].text
      self.pnr["Class"] = journeyDetails[7].text
   
   def getPassengerDetails(self, data):
      # this is actual passenger information
      trElements = data.getchildren()
      self.pnr["ChartingStatus"] = (trElements[-2].getchildren()[1].text).lstrip().rstrip()
       
      passenger = []
      for tr in trElements[1:-2]:
        passDict = {}
        td = tr.getchildren()
        passDict["Name"] = td[0].getchildren()[0].text
        passDict["BookingStatus"] = (td[1].getchildren()[0].text).lstrip().rstrip()
        passDict["CurrentStatus"] = td[2].getchildren()[0].text
        passenger.append(passDict)
      self.pnr["passenger"] = passenger
        
   def parseSuccess(self, root):
     successDataXpath = "//table[@width='100%' and @border='0' and @cellpadding='0' and @cellspacing='1' and @class='table_border']"
     dataElements = root.xpath(successDataXpath)
   
     for data in dataElements:
       if data.get("id") is None:
         # this is train information
         self.getJourneyDetails(data)
       else:
         self.getPassengerDetails(data)
         
   def parseFailure(self, root):
     failureXpath = "//td[@class='inside_heading_text' and @colspan='4' and @align='center' and @valign='top']"
     serverErrorXpath = "//h1"
     serverErrorString = "Sorry, This particular service is unavailable at this time!!!"
     
     e = root.xpath(serverErrorXpath)
     if len(e) == 1:
       if e[0].text == serverErrorString:
         self.pnr["Status"]["message"] = serverErrorString
         self.pnr["Status"]["code"] = RESPONSE_CODE_GENERAL_ERROR
         return
     
     e = root.xpath(failureXpath)
     p = e[0].getparent().getparent().getparent()
     c = p.getchildren()
     
     self.pnr["Status"]["code"] = RESPONSE_CODE_GENERAL_ERROR
     self.pnr["Status"]["message"] = c[2].text
   
   
   def parseHtml(self, result):
      try:
         root = html.fromstring(result)
         #root = html.parse("pnr_result.html")
         #root = html.parse("pnr_fail.html")
         successXpath = "//td[@class='Enq_heading' and @colspan='4' and @align='center' and @valign='top']"

         enqHeading = root.xpath(successXpath)
         if len(enqHeading) == 1:
           self.parseSuccess(root)
         else:
           self.parseFailure(root)
      except:
         self.pnr["Status"]["message"] = RESPONSE_MESSAGE_PARSE_ERROR
         self.pnr["Status"]["code"] = RESPONSE_CODE_PARSE_ERROR
         return
   
   def queryWeb(self, pnrNumber):
     return_object = {}
     lccp_pnrno1 = pnrNumber
     params = urllib.urlencode({'lccp_pnrno1': lccp_pnrno1, 'submitpnr': 'Get Status'})
     headers = {"Content-type": "application/x-www-form-urlencoded",
                "Host": "www.indianrail.gov.in",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-us,en;q=0.5",
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                "Keep-Alive": "115",
                "Connection": "keep-alive",
                "Referer": "http://www.indianrail.gov.in/pnr_stat.html",
                "Accept": "text/plain"}
     conn = httplib.HTTPConnection(INDIANRAIL_WEB_URL,80,timeout=INDIANRAIL_WEB_TIMEOUT)
     return_object = {}
     return_object['status'] = 'OK'
     return_object['data'] = {}
     try :
       conn.request("POST", INDIANRAIL_WEB_URL_PATH, params, headers)
       response = conn.getresponse()
       data = response.read()
       conn.close()
       return data
     except:
       pass
   
   def queryPnr(self, pnrno):
     self.pnr["PNR"] = pnrno
     result = self.queryWeb(pnrno)
     self.parseHtml(result)
     return self.pnr
   
      
if __name__ == '__main__':
  for pnrno in [4249727205, 4246884564, 4560301997, 4802979502, 4703019444, 4802979502, 4344195697, 4444195935]:
      pnrobject = PNRClass()
      print pnrobject.queryPnr(pnrno)
   
