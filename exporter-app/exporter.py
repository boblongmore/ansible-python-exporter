from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse, JSONResponse
from starlette.responses import Response
import httpx
import os
import uvicorn

load_dotenv()
AAP_URL = os.getenv('aap_server')
AAP_TOKEN = os.getenv('aap_token')
JOB_ID = 20
API_ENDPOINT=f"/api/controller/v2/job_templates/{JOB_ID}/jobs/"

print(API_ENDPOINT)

app = FastAPI()

async def get_job_details(query):
    url = f"https://{AAP_URL}{API_ENDPOINT}{query}"
    headers = {"Authorization": f"Bearer {AAP_TOKEN}"}
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    return 0

@app.get("/job_metrics")
async def job_metrics():
    successful = await get_job_details("?status=successful")
    failure = await get_job_details("?status=failed")
    job_metrics_prom = f"""
    # HELP ansible_job_template_run_success Number of successful template runs
    # TYPE ansible_job_template_run_success counter
    ansible_job_template_run_success {successful['count']}
    # HELP ansible_job_template_run_failure Number of failed template runs
    # TYPE ansible_job_template_run_failure counter
    ansible_job_template_run_failure {failure['count']}
    """
    return Response(content=job_metrics_prom, media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=5000)
