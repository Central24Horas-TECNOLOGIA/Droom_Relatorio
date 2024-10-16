'''
DROOM -
        Client_ID_DROOM = '3d824385cf984bd78eece82d741f3b7a'
        Client_Secret_DROOM = 'mgAJkZVXhpnHYMDsKn6BHMb_P0rWnJe-EYgsAM16rSkHj5-6QNwv2f4QZ5iTn8Fk3peO1YB2kiBoz4jYaOPtSQ'
        Autorização = Basic YTVjOWZhYjdkMDcwNGY5MDhiNDhlMDM3YmFmM2IyMDY6V1dNQnNrSmU3RTZhUWhJdzNxNXRrNkRvUnRfWUJ0dVNzNEVDcmt6aDkwVUc1ZTNKMm9vbVRfMWVrSUVrZ3Nrc1hMOEtqbWRyZWtWa0RMai1SOVhYNFE=
'''
import requests
from datetime import datetime
import base64
import json
import time
import csv
import  os

#Links
URL_API = "https://droom.talkdeskid.com/oauth/token"
|#URL_EXPLORE = "https://api.talkdeskapp.com/data/reports/type/jobs/id"
def data_formatada():
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    return data_hoje
def  Requisicao_Token():
    '''Client_ID_DROOM = '3d824385cf984bd78eece82d741f3b7a'
    Client_Secret_DROOM = 'mgAJkZVXhpnHYMDsKn6BHMb_P0rWnJe-EYgsAM16rSkHj5-6QNwv2f4QZ5iTn8Fk3peO1YB2kiBoz4jYaOPtSQ'
    Autorizacao_DROOM = base64.b64encode(bytes(f'{Client_ID_DROOM}:{Client_Secret_DROOM}', "UTF-8"))'''

    payload = {"grant_type": "client_credentials"}
    headers = {
        "accept": "application/json",
        "Authorization": "Basic YTVjOWZhYjdkMDcwNGY5MDhiNDhlMDM3YmFmM2IyMDY6V1dNQnNrSmU3RTZhUWhJdzNxNXRrNkRvUnRfWUJ0dVNzNEVDcmt6aDkwVUc1ZTNKMm9vbVRfMWVrSUVrZ3Nrc1hMOEtqbWRyZWtWa0RMai1SOVhYNFE=",
        "content-type": "application/x-www-form-urlencoded"
    }
    response = requests.post(URL_API, data=payload, headers=headers)
    data = json.loads(response.text)
    access_token = data['access_token']
    return access_token

def Job(token,data):
    url = "https://api.talkdeskapp.com/data/reports/contacts/jobs"
    payload = {"name": "contacts_numbers", "timezone": "America/Sao_Paulo", "format": "csv",
               "timespan": {"from": f"{data}T00:00:00Z", "to": f"{data}T23:59:59Z"}}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    response_jobs = requests.post(url, json=payload, headers=headers)
    data_string = response_jobs.text
    data_string = json.loads(response_jobs.text)
    job_id = data_string['job']['id']
    return job_id

def Download_job(job_id,data, token):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    url_download = "https://api.talkdeskapp.com/data/reports/contacts/files/" + job_id
    payload = {"name": "contacts_numbers", "timezone": "America/Sao_Paulo", "format": "csv",
               "timespan": {"from": f"{data}T00:00:00Z", "to": f"{data}T23:59:59Z"}}
    response_jobs = requests.get(url_download, json=payload, headers=headers)
    data_cv = response_jobs.text
    return data_cv
def CSV_TO_CSV(data_cv):
    header = [
        "Interaction ID", "Contact ID", "Company Number", "Phone Display Name", "Contact Person Number",
        "External Phone Number (Forward)", "Direction", "Contact Type", "Started At", "Wait Time",
        "Time to Missed", "Abandon Time", "Short Abandon Time", "Time to Voicemail", "Ring Time",
        "Connect Time", "Answered At", "Connected At", "Talk Time", "Hard Hold Time", "Soft Hold Time",
        "Hold Time", "After Call Work Time", "Finished At", "Duration", "Handle Time",
        "Inside Business Hours (Yes / No)", "Inside Service Level (Yes /No)",
        "Within Service Level Threshold (Yes / No)",
        "Transfer Out (Yes/No)", "Transfer Out Type", "Transfer In (Yes / No)", "Transfer In Type",
        "Callback (Yes / No)", "Ring Groups", "User Name", "Direct Assignment User", "Team Name",
        "User ID", "Direct Assignment IDs", "Team ID", "Handling Ring Groups", "Disconnected By Agent",
        "Last Contact (Yes / No)", "Data Status (Valid / Damaged)"
    ]
    data_lines = data_cv.strip().split('\n')
    data = [line.split(',') for line in data_lines]
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = fr"//192.168.5.21/BCMS/Monitor Skill/ListTalkdesk/100/Calls_reporte_{data_hoje}.csv"
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

    print(f"Arquivo CSV '{nome_arquivo}' criado com sucesso.")

#Execução
try:
    Data = data_formatada()
    Tolken = Requisicao_Token()
    Id = Job(Tolken, Data)
    time.sleep(5)
    Data_cv = Download_job(Id,Data,Tolken)
    CSV_TO_CSV(Data_cv)
except:
    print("Ocorreu algum erro durante o processo...tentando novamente.")
    time.sleep(60)
    Data = data_formatada()
    Tolken = Requisicao_Token()
    Id = Job(Tolken, Data)
    time.sleep(5)
    Data_cv = Download_job(Id, Data, Tolken)
    CSV_TO_CSV(Data_cv)