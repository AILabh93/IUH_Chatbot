import os
import threading
from threading import Thread
from time import sleep

def run_rasa():
    os.chdir('rasa/')
    os.system('fuser -k 5005/tcp')
    os.system('rasa run --endpoints endpoints.yml --credentials credentials.yml & rasa run actions')

def run_server():
    sleep(60)
    print('loading server')
    os.chdir('../Backend')
    os.system('python3 manage.py runserver')

t1 = threading.Thread(target=run_rasa)
t2 = threading.Thread(target=run_server)
t1.start()
t2.start()
