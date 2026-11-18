import os
import socket
from flask import Flask, jsonify
import redis

app = Flask(__name__)
redis_host = os.getenv("REDIS_HOST", "redis")
cache = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.route("/")
def status():
    hits = cache.incr("api_hits")
    return jsonify({
        "service": "cloud-lab-status-api",
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "container_id": socket.gethostname(),
        "architecture": os.uname().machine,
        "total_requests": hits
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
