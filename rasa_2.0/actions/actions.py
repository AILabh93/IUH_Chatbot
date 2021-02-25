# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted
from bs4 import BeautifulSoup
import requests
import lxml
import bs4
import gc
from fasttext import load_model

model = load_model('actions/model_chuyen_nganh.bin')


def predict_monhoc(text):
    label = model.predict(text)
    return label[0][0][-4:]


class action_luong(Action):
    def name(self):
        return 'action_luong'

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(template='utter_'+mon_hoc+'_luong')
        if mon_hoc == 'khdl':
            dispatcher.utter_message(image=str(
                'https://nordiccoder.com/app/uploads/2020/01/Screenshot-at-Jan-10-14-56-18.png'))
        elif mon_hoc == 'cntt':
            dispatcher.utter_message(
                image=str('https://btec.fpt.edu.vn/wp-content/uploads/2019/07/2-1.jpg'))
        elif mon_hoc == 'ktpm':
            dispatcher.utter_message(image=str(
                'https://easyuni.com/media/uploads/2019/06/21/software-engineer-salary-worldwide-201920190226.png'))
        elif mon_hoc == 'khmt':
            dispatcher.utter_message(image=str(
                'https://media.bitdegree.org/storage/media/images/2020/01/computer-science-salary-entry-300x259.png'))
        return []


def createButton():
    temp_button_lst = []

    temp_button_lst.append({
        "type": "postback",
        "title": "Khoa học máy tính",
        "payload": "tư vấn khmt"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "Kĩ thuật phần mềm",
        "payload": "tư vấn ktpm"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "Công nghệ thông tin",
        "payload": "tư vấn cntt"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "Hệ thống thông tin",
        "payload": "tư vấn httt"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "Khoa học dữ liệu",
        "payload": "tư vấn khdl"
    })

    return temp_button_lst


class action_but(Action):
    def name(self):
        return 'action_but'

    def run(self, dispatcher, tracker, domain):
        but = createButton()
        dispatcher.utter_message(text="Bạn cần tư vấn gì", buttons=but)
        return []


class action_unknown(Action):
    def name(self):
        return "action_unknown"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text='Xin lỗi mình chưa hiểu ý bạn')
        but = createButton()
        dispatcher.utter_message(
            text="Bạn có thể chọn các chuyên ngành sau", buttons=but)

        return []


class action_tuvan(Action):
    def name(self):
        return "action_tuvan"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(template='utter_tuvan_'+mon_hoc)
        return []


class action_vieclam(Action):
    def name(self):
        return "action_vieclam"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(template='utter_'+mon_hoc+'_vieclam')
        return []


class action_tilesvratruong(Action):
    def name(self):
        return "action_tilesvratruong"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(template='utter_'+mon_hoc+'_tilesvratruong')
        return []


class action_canhtranh(Action):
    def name(self):
        return "action_canhtranh"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(template='utter_'+mon_hoc+'_canhtranh')
        return []


class action_tailieu(Action):
    def name(self):
        return "action_tailieu"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(template='utter_'+mon_hoc+'_tailieu')
        return []


class action_dinhhuongsai(Action):
    def name(self):
        return "action_dinhhuongsai"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(template='utter_'+mon_hoc+'_dinhhuongsai')
        return []


class action_ungdung(Action):
    def name(self):
        return "action_ungdung"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(template='utter_'+mon_hoc+'_ungdung')
        return []


class action_linhvuc(Action):
    def name(self):
        return "action_linhvuc"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_linhvuc')
        return []


class action_monhoc(Action):
    def name(self):
        return "action_monhoc"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_khmt_'+mon_hoc)
        return []


class action_kienthuccancokhiratruong(Action):
    def name(self):
        return "action_kienthuccancokhiratruong"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_khmt_'+mon_hoc)
        return []


class action_giangvien(Action):
    def name(self):
        return "action_giangvien"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_giangvien')
        return []


class action_ngonngu(Action):
    def name(self):
        return "action_ngonngu"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_ngonngu')
        return []


class action_laptrinh(Action):
    def name(self):
        return "action_laptrinh"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_laptrinh')
        return []


# code


class action_nu(Action):
    def name(self):
        return "action_nu"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_nu')
        return []


class action_diemso(Action):
    def name(self):
        return "action_diemso"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_diemso')
        return []


class action_chatluonggiaovien(Action):
    def name(self):
        return "action_chatluonggiaovien"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(
            template='utter_'+mon_hoc+'_chatluonggiaovien')
        return []


class action_baitaplon(Action):
    def name(self):
        return "action_baitaplon"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_baitaplon')
        return []


class action_yeucau_tienganh(Action):
    def name(self):
        return "action_yeucau_tienganh"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_yeucau_tienganh')
        return []


class action_tinhcach(Action):
    def name(self):
        return "action_tinhcach"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_tinhcach')
        return []


class action_thuctap(Action):
    def name(self):
        return "action_thuctap"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_thuctap')
        return []


class action_hocphi(Action):
    def name(self):
        return "action_hocphi"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_hocphi')
        return []


class action_chatluongcao(Action):
    def name(self):
        return "action_chatluongcao"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_chatluongcao')
        return []


class action_lotrinhhoc(Action):
    def name(self):
        return "action_lotrinhhoc"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_lotrinhhoc')
        return []


class action_dungcuhoctap(Action):
    def name(self):
        return "action_dungcuhoctap"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_dungcuhoctap')
        return []


class action_xuhuong(Action):
    def name(self):
        return "action_xuhuong"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_xuhuong')
        return []


class action_cachhoc(Action):
    def name(self):
        return "action_cachhoc"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_cachhoc')
        return []


class action_phongvan(Action):
    def name(self):
        return "action_phongvan"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_phongvan')
        return []


class action_kienthuc(Action):
    def name(self):
        return "action_kienthuc"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_kienthuc')
        return []


class action_yeucau(Action):
    def name(self):
        return "action_yeucau"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_yeucau')
        return []


class action_thuchanh(Action):
    def name(self):
        return "action_thuchanh"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_thuchanh')
        return []


class action_daotao(Action):
    def name(self):
        return "action_daotao"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_daotao')
        return []


class action_kynang(Action):
    def name(self):
        return "action_kynang"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])

        dispatcher.utter_message(template='utter_'+mon_hoc+'_kynang')
        return []


class action_doantotnghiep(Action):
    def name(self):
        return "action_doantotnghiep"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(template='utter_'+mon_hoc+'_doantotnghiep')
        return []


class action_tinchi(Action):
    def name(self):
        return "action_tinchi"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(template='utter_'+mon_hoc+'_tinchi')
        return []


class action_thuctapdoanhnghiep(Action):
    def name(self):
        return "action_thuctapdoanhnghiep"

    def run(self, dispatcher, tracker, domain):
        mon_hoc = predict_monhoc(tracker.latest_message['text'])
        dispatcher.utter_message(
            template='utter_'+mon_hoc+'_thuctapdoanhnghiep')
        return []
