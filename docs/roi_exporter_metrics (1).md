# ROI Metrics in Prometheus + FastAPI Exporter

*Date: 2025-04-18*

---

## ✅ Overview

This document outlines how to add ROI (Return on Investment) metrics to a FastAPI Prometheus exporter and how to calculate **time-windowed ROI** using Prometheus and Grafana.

---

## 🚀 Exporter Setup (FastAPI)

Here’s how your current exporter is structured:

- You pull job run data from AAP using FastAPI and HTTPX.
- You calculate hours and money saved by automation.
- You calculate IRR over three years using `numpy_financial`.
- You expose metrics via Prometheus text format at `/job_metrics`.

### 🧩 Add ROI Metric

Add this inside your FastAPI route:

```python
investment_cost = -INITIAL_INVESTMENT  # Convert to positive
roi = (money_saved - investment_cost) / investment_cost if investment_cost > 0 else 0
```

Then add to the output block:

```text
# HELP ansible_job_template_roi_calc Return on Investment for project
# TYPE ansible_job_template_roi_calc gauge
ansible_job_template_roi_calc {float(roi):.4f}
```

---

## 📈 Time-Windowed ROI in Prometheus

To calculate ROI **over a specific time window**, like the past 30 days:

### ✅ Step 1: Expose Cumulative Metrics

Add these lines to your exporter:

```text
# HELP project_investment_cost Total cost of investment
# TYPE project_investment_cost counter
project_investment_cost 500000.00

# HELP project_automation_gain Cumulative money saved
# TYPE project_automation_gain counter
project_automation_gain {float(money_saved):.2f}
```

### ✅ Step 2: Use PromQL for Rolling ROI

Example PromQL for 30-day ROI:

```promql
(rate(project_automation_gain[30d]) - rate(project_investment_cost[30d]))
/ rate(project_investment_cost[30d])
```

You can change `[30d]` to `[7d]`, `[365d]`, etc., in Grafana panels.

---

## 🔁 Summary

| Task                        | Recommendation                  |
|-----------------------------|----------------------------------|
| ROI calculation             | In Python (simpler, centralized) |
| Time-windowed ROI tracking | In Prometheus + Grafana          |
| Historical trends           | Use PromQL with rate()/increase()|

---

Let me know if you want this converted to PDF or need help building the Grafana dashboard!
