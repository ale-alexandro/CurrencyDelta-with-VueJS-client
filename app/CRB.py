import requests
import xmltodict

class CRB:
    def __init__(self):
        pass

    def getCurrList(self):
        data = xmltodict.parse(requests.get("http://www.cbr.ru/scripts/XML_valFull.asp?d=0").text)['Valuta']['Item']
        response = []
        for req_currency in data:
            currency = {}
            if req_currency['ISO_Char_Code'] != None:
                currency['ID'] = req_currency['@ID']
                currency['Name'] = req_currency['Name']
                currency['ISO_Char_Code'] = req_currency['ISO_Char_Code']
                response.append(currency)
        return {'data': response}

    def getDelta(self, cur, dateStart, dateEnd):
        dateStart = "{}/{}/{}".format(dateStart[0:2], dateStart[3:5], dateStart[6:10])
        dateEnd = "{}/{}/{}".format(dateEnd[0:2], dateEnd[3:5], dateEnd[6:10])

        data = xmltodict.parse(requests.get("http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date1}&date_req2={date2}&VAL_NM_RQ={cid}".format(cid=cur, date1=dateStart, date2=dateEnd)).text)

        if dateStart != dateEnd: 
            return {'delta': float(data['ValCurs']['Record'][-1]['Value'].replace(',', '.')) - float(data['ValCurs']['Record'][0]['Value'].replace(',', '.')), 'start': data['ValCurs']['Record'][0]['Value'], 'end':data['ValCurs']['Record'][-1]['Value']}
        else:
            return {'delta': 0, 'start': data['ValCurs']['Record']['Value'], 'end':data['ValCurs']['Record']['Value']}