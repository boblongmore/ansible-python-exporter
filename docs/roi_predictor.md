# 📈 Predictive ROI with FastAPI, Prophet & Prometheus

This guide extends your existing FastAPI app that calculates ROI to include **ROI forecasting** using [Prophet](https://facebook.github.io/prophet/) and push results to **Prometheus Pushgateway** for Grafana visualization.

---

## 📦 Requirements

Install dependencies:

```bash
pip install pandas prophet prometheus_client
