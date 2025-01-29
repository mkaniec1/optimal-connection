## About Project
In telecommunication data can be sent using one of many frequencies. Turns out there is 4.8 THz range of freqencies that guarantees the most stable signal with the least amount of interferances. This range is really valuable for companies so optimizing its usage is a crucial task. This app uses A* algorithm to find the optimal way to reserve space for connection between two stations. User interface is created in React and A* algorithm is implemented in python. Backend web framework is Django.

## Install Dependencies
### Django:
Necessary packages are listed in backend/pop/requirements.txt.
To install them use:
```bash
cd backend/pop
pip install -r requirements.txt
```
## Loading Data
To use data provided in csv files you need to create database first.
Go to backend/pop and type:
```bash
python manage.py migrate
```
This will create db.sqlite3 file containing necessary entities.
Now it's time to load data. Launch Django shell by typing:
```bash
python manage.py shell
```
Inside the shell execute lines:
```python
from optimal_path.load_data import load_all
load_all()
exit()
```
## Run App
In order to run app in development mode you have to launch
backend Django server and React separately.
Django:
```bash
cd backend/pop
python manage.py runserver
```
React (in other terminal):
```bash
cd frontend
npm start
```
