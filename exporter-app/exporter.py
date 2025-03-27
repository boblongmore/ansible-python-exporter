from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime
import numpy_financial as npf
import httpx
import os
import uvicorn

load_dotenv()
AAP_URL = os.getenv('aap_server')
AAP_TOKEN = os.getenv('aap_token')
JOB_ID = 20
API_ENDPOINT=f"/api/controller/v2/job_templates/{JOB_ID}/jobs/"
EST_MANUAL_TIME = 60 # Time to do the task manually in minutes
EST_ENG_COST = 65 # Hourly rate of an engineer
INITIAL_INVESTMENT = -500000



app = FastAPI()

async def get_job_details(query):
    url = f"https://{AAP_URL}{API_ENDPOINT}{query}"
    headers = {"Authorization": f"Bearer {AAP_TOKEN}"}
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    return 0

async def auto_hours_saved(successful):
    manual_time = EST_MANUAL_TIME * successful['count']
    run_duration_total = 0
    for jobs in successful['results']:
        start = datetime.fromisoformat(jobs['started'])
        finish = datetime.fromisoformat(jobs['finished'])
        duration = finish - start
        run_duration_total += duration.seconds
    automation_time = run_duration_total / 60
    return (manual_time / 60) - (automation_time / 60)

async def auto_money_saved(successful):
    manual_time = EST_MANUAL_TIME * successful['count']
    manual_cost = (manual_time / 60) * EST_ENG_COST
    run_duration_total = 0
    for jobs in successful['results']:
        start = datetime.fromisoformat(jobs['started'])
        finish = datetime.fromisoformat(jobs['finished'])
        duration = finish - start
        run_duration_total += duration.seconds
    automation_time = run_duration_total / 60
    automation_cost = (automation_time / 60) * EST_ENG_COST
    return (manual_cost - automation_cost)

async def calc_irr(successful):
    savings = await auto_money_saved(successful)
    irr = npf.irr([INITIAL_INVESTMENT, savings, savings, savings])
    irr_value = irr * 100
    return irr_value



@app.get("/job_metrics", response_class=PlainTextResponse)
async def job_metrics():
    successful = await get_job_details("?status=successful")
    failure = await get_job_details("?status=failed")
    hours_saved = await auto_hours_saved(successful)
    money_saved = await auto_money_saved(successful)
    irr_calc = await calc_irr(successful)
    job_metrics_prom = f"""
# HELP ansible_job_template_run_success Number of successful template runs
# TYPE ansible_job_template_run_success counter
ansible_job_template_run_success {successful['count']}
# HELP ansible_job_template_run_failure Number of failed template runs
# TYPE ansible_job_template_run_failure counter
ansible_job_template_run_failure {failure['count']}
# HELP ansible_job_template_hours_saved Number of hours saved by automating tasks
# TYPE ansible_job_template_hours_saved counter
ansible_job_template_hours_saved {float(hours_saved):.2f}
# HELP ansible_job_template_money_saved Amount of money saved by automating tasks
# TYPE ansible_job_template_money_saved counter
ansible_job_template_money_saved {float(money_saved):,.2f}
# HELP ansible_job_template_irr_calc Calculated IRR for three years
# TYPE ansible_job_template_irr_calc counter
ansible_job_template_irr_calc {float(irr_calc):.2%}
    """
    return job_metrics_prom

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=5000)
