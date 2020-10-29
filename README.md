# Currency Delta
Currency Delta is a test task (oh, really) flask microservice that pulls data from *cbr.ru* website with python. For this solution i used:
  
  - Python
  - Flask
  - Python requests
  - VueJS

## Features!
##### - Pulls List of currencies with ISO Code (RUB, EUR, etc.) and send it to you in json
```%url_of_server%/api/getCurrencyList```
**args**: none
**return value**: JSON Object with currencies data
**example answer**:
`{"data": [{"ID": "R01010","ISO_Char_Code": "AUD","Name": "Австралийский доллар"}, ... {"ID": "R01820","ISO_Char_Code": "JPY","Name": "Японская иена"}]}`
******
##### - Pulls selected currency value by date range and calcs delta from cbr.ru
```%url_of_server%/api/getCurrencyDelta```
**args**:
  - ***cur***: Internal Currency ID from cbr.ru. E.g. R01235 is USD
  - ***start***: Start Date in format DD-MM-YYYY 
  - ***end***: End Date in format DD-MM-YYYY 
    - ***end*** >= ***start***
   
  
**return value**: JSON object with delta, currency value at start date and currency value at end date
**example request and answer**:
```/api/getCurrencyDelta?cur=R01235&start=02-03-2011&end=05%2F05%2F2016``` 
```{"delta": 37.4149, "end": "66,1718", "start": "28,7569"}```


# How it Works
When you make request to ```api/getCurrencyList```, service pulls data in XML from cbr [example xml](http://www.cbr.ru/scripts/XML_val.asp?d=0), parse it with [xmltodict](https://pypi.org/project/xmltodict/) to dict, drops all currencies with null ISO Code and send it to you

When you make request to ```api/getCurrencyList```, service pulls data in XML from (cbr.ru)[example xml](http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=02/03/2001&date_req2=14/03/2001&VAL_NM_RQ=R01235) and if start date != end date retruns delta and currencies for dates. Else, delta is 0 (start date currency equal to end date currency).


### Installation
TestTask requires [Node.js](https://nodejs.org/) and [Python](https://www.python.org).

Install the dependencies and start the dev server of service(backend).
```bash
$ python3 -m pip install -r requirements.txt
$ flask run
```
Install the dependencies and start the dev server of service(frontend).
```bash
$ cd static
$ npm install
$ npm run dev
```
Build the VueJS app via webpack.
```bash
$ cd static
$ npm install
$ npm run build
```

On main branch you have prod version
To run production
```bash
$ python3 -m pip install gunicorn
$ gunicorn --bind 0.0.0.0:80 CurrencyDelta:app
```

# License
----

MIT
