import httpx
from dotenv import load_dotenv
import os

load_dotenv()
AAP_URL = os.getenv('aap_server')
AAP_TOKEN = os.getenv('aap_token')
JOB_ID = '20'
API_ENDPOINT=f"/api/controller/v2/job_templates/{JOB_ID}/jobs/"

def get_aap():
    headers = {"Authorization": f"Bearer {AAP_TOKEN}"}
    print(headers)
    url = f"https://{AAP_URL}{API_ENDPOINT}"
    print(url)
    response = httpx.get(url, verify=False, headers=headers)
    print(response.json())

def get_job_details():
    url = f"https://{AAP_URL}{API_ENDPOINT}"
    headers = {"Authorization": f"Bearer {AAP_TOKEN}"}
    response = httpx.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return response.json()

if __name__ == "__main__":
    data = get_job_details()
    print(data)
