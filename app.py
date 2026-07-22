#comment
from flask import Flask, jsonify, render_template_string
import json
import platform
import os
import psutil # Ensure psutil is installed if you want real metrics, or fallback safely

app = Flask(__name__)

# Basic system diagnostics generator logic
def get_diagnostics():
    try:
        cpu_load = psutil.cpu_percent(interval=0.5)
        memory_usage = psutil.virtual_memory().percent
    except Exception:
        cpu_load = 0.0
        memory_usage = 0.0

    return {
        "status": "UP",
        "platform": platform.system(),
        "platform_release": platform.release(),
        "architecture": platform.machine(),
        "environment": os.getenv("APP_ENV", "production"),
        "metrics": {
            "cpu_usage_percent": cpu_load,
            "memory_usage_percent": memory_usage
        }
    }

# HTML Template Embedded to avoid multi-file orchestration dependencies
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevSecOps Kubernetes Pod Dashboard</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 40px; }
        .card { background-color: #1e293b; border-radius: 12px; padding: 24px; max-width: 600px; margin: 0 auto; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); border: 1px solid #334155; }
        h1 { color: #38bdf8; font-size: 24px; margin-top: 0; border-bottom: 2px solid #334155; padding-bottom: 12px; }
        .badge { background-color: #22c55e; color: white; padding: 4px 12px; border-radius: 9999px; font-weight: bold; font-size: 14px; }
        .metric-group { margin-top: 20px; }
        .metric { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #334155; }
        .metric:last-child { border-bottom: none; }
        .label { color: #94a3b8; }
        .value { font-family: monospace; font-weight: bold; color: #e2e8f0; }
        pre { background-color: #0f172a; padding: 12px; border-radius: 6px; overflow-x: auto; border: 1px solid #334155; color: #38bdf8; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 DevSecOps Live Cluster Deployment Status</h1>
        <div class="metric">
            <span class="label">Application Health Status:</span>
            <span class="badge">ONLINE</span>
        </div>
        
        <div class="metric-group">
            <h3>🖥️ System Infrastructure Details:</h3>
            <div class="metric"><span class="label">Operating System Host:</span><span class="value">{{ data.platform }} ({{ data.architecture }})</span></div>
            <div class="metric"><span class="label">Runtime Deployment State:</span><span class="value">{{ data.environment }}</span></div>
            <div class="metric"><span class="label">CPU Execution Overhead:</span><span class="value">{{ data.metrics.cpu_usage_percent }}%</span></div>
            <div class="metric"><span class="label">Container Ram Memory:</span><span class="value">{{ data.metrics.memory_usage_percent }}%</span></div>
        </div>
        
        <div class="metric-group">
            <h3>📊 Raw JSON Telemetry Pipeline Feed:</h3>
            <pre>{{ raw_json }}</pre>
        </div>
    </div>
</body>
</html>
"""

# Web server root traffic listener gateway route
@app.route('/')
def home():
    data = get_diagnostics()
    raw_json = json.dumps(data, indent=2)
    return render_template_string(HTML_TEMPLATE, data=data, raw_json=raw_json)

# K8s Health Check Probes Endpoint Route (Highly Recommended practice)
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    print("[INFO] Python Web Server Engine initialization sequence triggered.", flush=True)
    print("[INFO] Application running target binding: Host 0.0.0.0, Port 80", flush=True)
    
    # Port 80 is required to perfectly align with your k8s targetPort configuration mapping parameters
    app.run(host='0.0.0.0', port=80, debug=False)
