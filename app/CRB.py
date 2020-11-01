from flask import json

import requests
import xmltodict

from app import db
from app.models import Currency, Value

class CRB:
    def __init__(self):
        pass

    def __json_currency(self, curr_list):
        result = []
        for curr in curr_list:
            c = {}
            c['Name'] = curr.name
            c['ISO_Char_Code'] = curr.char_code
            c['ID'] = curr.cbr_id
            result.append(c)
        return json.dumps({'data': result})

    def getCurrList(self):
        cl = Currency.query.all()
        if len(cl) != 0:
            return self.__json_currency(cl)
        
        data = xmltodict.parse(requests.get("http://www.cbr.ru/scripts/XML_valFull.asp?d=0").text)['Valuta']['Item']
        response = []
        for req_currency in data:
            currency_dict = {}
            if not Currency.query.filter_by(char_code = req_currency['ISO_Char_Code']).first(): # Sometimes crb send doubles
                db.session.add(Currency(cbr_id = req_currency['@ID'], char_code = req_currency["ISO_Char_Code"] if req_currency["ISO_Char_Code"] else "", name = req_currency['Name']))
                db.session.commit()
                    
                currency_dict['ID'] = req_currency['@ID']
                currency_dict['Name'] = req_currency['Name']
                currency_dict['ISO_Char_Code'] = req_currency['ISO_Char_Code']
                response.append(currency_dict)
        return json.dumps({'data': response})

    def getDelta(self, cur, dateStart, dateEnd):
        valStart = 0
        valEnd = 0
        if not Value.query.filter_by(cbr_id=cur, timestamp=dateStart).first():
            data = xmltodict.parse(requests.get("http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date1}&date_req2={date2}&VAL_NM_RQ={cid}".format(cid=cur, date1=dateStart, date2=dateStart)).text)['ValCurs']
            print(data)
            if not 'Record' in data.keys():
                return {'error': 1, 'date': dateStart}

            value = Value(cbr_id=cur, timestamp=dateStart, val_rel_to_rub=float(data['Record']['Value'].replace(",", ".")))
            db.session.add(value)
            db.session.commit()

        if not Value.query.filter_by(cbr_id=cur, timestamp=dateEnd).first(): # We dont need to request value for dateEnd if it equals to dateStart
            data = xmltodict.parse(requests.get("http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date1}&date_req2={date2}&VAL_NM_RQ={cid}".format(cid=cur, date1=dateEnd, date2=dateEnd)).text)['ValCurs']
            print(data)
            if not 'Record' in data.keys():
                return {'error': 1, 'date': dateEnd}
            
            value = Value(cbr_id=cur, timestamp=dateEnd, val_rel_to_rub=float(data['Record']['Value'].replace(",", ".")))
            db.session.add(value)
            db.session.commit()
        
        # Also we can upload all Range like this
        # if not Value.query.filter_by(cbr_id=cur, timestamp=dateStart).first() and Value.query.filter_by(cbr_id=cur, timestamp=dateEnd).first():
        #     data = xmltodict.parse(requests.get("http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date1}&date_req2={date2}&VAL_NM_RQ={cid}".format(cid=cur, date1=dateStart, date2=dateEnd)).text)
        #     for record in data['ValCurs']['Record']:
        #         if not Value.query.filter_by(cbr_id=cur, timestamp=record['@Date'].replace(".", "/")).first()
        #             value = Value(cbr_id=cur, timestamp=record['@Date'].replace(".","/"), val_rel_to_rub=float(record['Value'].replace(',', '.')))
        #             db.session.add(value)
        #             db.session.commit()

        valStart = Value.query.filter_by(cbr_id=cur, timestamp=dateStart).first().val_rel_to_rub
        if dateStart != dateEnd: 
            valEnd = Value.query.filter_by(cbr_id=cur, timestamp=dateEnd).first().val_rel_to_rub
            return {'delta': valEnd - valStart, 'start': valStart, 'end': valEnd}
        else:
            return {'delta': 0, 'start': valStart, 'end': valStart}