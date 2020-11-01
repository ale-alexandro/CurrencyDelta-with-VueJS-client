# Currency Delta
Currency Delta is a test task (oh, really) flask microservice that pulls data from *cbr.ru* website with python. For this solution i used:
  
  - Python
  - Flask
  - SQLAlchemy
  - Python requests
  - VueJS

## Features!
##### - Pulls List of currencies with ISO Code (RUB, EUR, etc.) and send it to you in json
```%url_of_server%/api/getCurrencyList```

**args**: none

**return value**: JSON Object with currencies data

**errors**: none

**example answer**: `{"data": [{"ID": "R01010","ISO_Char_Code": "AUD","Name": "Австралийский доллар"}, ... {"ID": "R01820","ISO_Char_Code": "JPY","Name": "Японская иена"}]}`
******
##### - Pulls selected currency value by date range and calcs delta from cbr.ru
```%url_of_server%/api/getCurrencyDelta```

**args**:
  - ***cur***: Internal Currency ID from cbr.ru. E.g. R01235 is USD
  - ***start***: Start Date in format DD-MM-YYYY 
  - ***end***: End Date in format DD-MM-YYYY 
  
**errors**: 
  - ***Code 1***: Not Found data for date. CRB has no data for the date. Returns date
    - ```{"error": "1", "date": "01-01-1995"}``` for ```/api/getCurrencyDelta?cur=R01235&start=01-01-1995&end=01-01-2020``` 
  - ***Code 2***: Incorrect begin date. 
    - ```{"error": "2", "date": "31.11.199"}``` for ```/api/getCurrencyDelta?cur=R01235&start=31-11-199&end=01-01-2020``` 
  - ***Code 3***: Incorrect end date. 
    - ```{"error": "3", "date": "01/10/2020"}``` for ```/api/getCurrencyDelta?cur=R01235&start=01-01-2020&end=01/10/2020``` 
  - ***Code 4***: Incorrect(or Nonexistent) CRB Currecy code. 
    - ```{"error": "4", "date": "R00000"}``` for ```/api/getCurrencyDelta?cur=R00000&start=01-01-2020&end=10-01-2020``` 
   
  
**return value**: JSON object with delta, currency value at start date and currency value at end date

**example request and answer**:
```/api/getCurrencyDelta?cur=R01235&start=02-03-2011&end=05%2F05%2F2016``` 
```{"delta": 37.4149, "end": "66,1718", "start": "28,7569"}```


# How it Works
When you make request to ```api/getCurrencyList```, firstly service pulls data in XML from cbr [example xml](http://www.cbr.ru/scripts/XML_val.asp?d=0), parse it with [xmltodict](https://pypi.org/project/xmltodict/) to dict, drops all currencies doubles, save it into sqlite db and send it to client. And if the data in the database has already been saved, then the service simply serializes from into JSON and delivers to the client

When you make request to ```api/getCurrencyDelta```, service checks the database for a currency value for the given date at. If one of the values is missing, it requests it from crb [example xml](http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=02/03/2001&date_req2=02/03/2001&VAL_NM_RQ=R01235) and saves it to the database. Then it sends the delta between End and Start, and the values for dateStart and dateEnd to the client

### Installation
TestTask requires [Node.js](https://nodejs.org/) and [Python](https://www.python.org).

Install the dependencies, deploy sqllite database and start the dev server of service(backend).
```bash
$ python3 -m pip install -r requirements.txt
$ flask db init 
$ flask db migrate
$ flask db upgrate 
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

To run production
In %basedir/%app/static
```bash
$ cd static
$ npm install
$ npm run build
```
In %basedir%
```bash
$ python3 -m pip install gunicorn
$ gunicorn --bind 0.0.0.0:80 CurrencyDelta:app
```

# License
----

MIT
