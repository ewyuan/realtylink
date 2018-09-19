# real-estate-scraper
A web scraper that aggregates real estate data from http://www.realtylink.org.
## Getting started

### Prerequisites
* Python 3
* schedule https://pypi.org/project/schedule/
* pandas https://pypi.org/project/pandas/
* requests https://pypi.org/project/requests/
* lxml https://pypi.org/project/lxml/

### How to run
1. Change to the realtylink directory.
2. Configure ./realtylink/config.py (Please view the documentation inside of config.py).
3. Enter the following:
```
>> pip3 install -r requirements.txt
>> python3 ./realtylink/main.py
```
To run the program continuously:
```
>> sudo nohup python3 ./realtylink/main.py &
```

## Sample output:
Please see ./realtylink/files/ for sample output files.
