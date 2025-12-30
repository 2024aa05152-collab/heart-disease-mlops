# Heart Disease Prediction API - Monitoring & Logging System

**Complete MLOps monitoring solution with Prometheus + Grafana for the Heart Disease Prediction API**

---

## 📋 What's Included

### 1. **Structured Logging** 
   - JSON-formatted logs for machine parsing
   - File-based rotating logs (api.log, errors.log, structured.json)
   - Real-time console output
   - Full request/response/error tracking

### 2. **Prometheus Metrics**
   - 15+ metrics tracking API and model performance
   - Request counting and latency tracking
   - Error rate monitoring
   - Model prediction metrics
   - Container resource metrics (via cAdvisor)

### 3. **Grafana Dashboard**
   - 10 auto-provisioned visualization panels
   - Real-time updates (10-second refresh)
   - Line charts, pie charts, gauges, and histograms
   - Performance trend analysis

### 4. **Docker Infrastructure**
   - Multi-container stack with Docker Compose
   - Health checks for all services
   - Persistent data storage
   - Network isolation

---

## 🚀 Quick Start (2 minutes)

```bash
# 1. Start all services
docker-compose up -d

# 2. Wait for services to be healthy
sleep 10
docker-compose ps

# 3. Open in browser
# API:        http://localhost:8000
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000 (admin/admin123)

# 4. Test with sample requests
bash test_monitoring.sh
```

---

## 🎯 Key Features

✅ **Real-time Monitoring** - Metrics updated every 15 seconds
✅ **Visual Dashboards** - 10-panel Grafana dashboard
✅ **Error Tracking** - Comprehensive error logging
✅ **Performance Metrics** - Request latency, throughput, errors
✅ **Model Monitoring** - Prediction rates and distribution
✅ **Auto-provisioning** - Grafana configured automatically
✅ **Production-Ready** - Following MLOps best practices
✅ **Easy Testing** - Automated test scripts included

---

## 📁 Files Created

### Core Implementation
```
src/
├── logging_config.py      # Logging configuration (230 lines)
└── metrics.py             # Prometheus metrics (170 lines)

app/
└── main.py               # Enhanced API with logging/metrics (290 lines)

monitoring/
├── prometheus.yml        # Prometheus configuration
└── grafana/
    ├── provisioning/     # Grafana auto-provisioning
    └── dashboards/
        └── heart-disease-dashboard.json  # 10-panel dashboard
```

### Configuration
```
Dockerfile                # Updated for monitoring
docker-compose.yml        # Complete stack orchestration
requirements.txt          # Added monitoring packages
```

### Documentation
```
MONITORING.md                      # Complete guide (500+ lines)
MONITORING_QUICK_REFERENCE.md      # Quick reference (300+ lines)
IMPLEMENTATION_SUMMARY.md          # Implementation details (400+ lines)
ARCHITECTURE_DIAGRAM.md            # System architecture (400+ lines)
IMPLEMENTATION_CHECKLIST.md        # Verification checklist
```

### Testing
```
test_monitoring.sh                 # Bash test script (10 tests)
test_monitoring_advanced.py        # Python test script (7 tests)
```

---

## 📊 Metrics Overview

### API Performance Metrics
- `heart_api_requests_total` - Total requests by method/endpoint/status
- `heart_api_request_duration_seconds` - Request latency (histogram)
- `heart_api_request_size_bytes` - Request payload size
- `heart_api_response_size_bytes` - Response payload size
- `heart_api_errors_total` - Error count by type
- `heart_api_active_requests` - Current in-flight requests

### Model Performance Metrics
- `heart_model_predictions_total` - Total predictions
- `heart_model_prediction_duration_seconds` - Inference time
- `heart_disease_predictions` - Risk distribution (at_risk/no_risk)
- `heart_disease_average_probability` - Average confidence
- `heart_model_loaded` - Model availability status (1/0)

---

## 📈 Dashboard Panels (10 Total)

1. **API Request Rate** - Requests per second
2. **API Latency Percentiles** - P95 & P99 latency
3. **Model Prediction Rate** - Predictions per second
4. **Risk Prediction Distribution** - Pie chart (at_risk vs no_risk)
5. **Model Loaded Status** - Gauge (loaded/failed)
6. **Active Requests** - Current request count
7. **Total Errors (5m)** - Error count in last 5 minutes
8. **Average Risk Probability** - Confidence trend
9. **Error Rate by Type** - Error distribution
10. **Request/Response Sizes** - Payload monitoring

---

## 🔍 Viewing Logs

```bash
# API operations
tail -f logs/api.log

# Errors only
tail -f logs/errors.log

# JSON structured logs
tail -f logs/structured.json | jq '.'

# From Docker container
docker-compose logs -f heart-api
```

---

## 🧪 Testing

### Automated Tests
```bash
# Bash script (10 tests, includes load testing)
bash test_monitoring.sh

# Python script (7 comprehensive tests)
python test_monitoring_advanced.py
```

### Manual Test
```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 50, "sex": 1, "cp": 0, "trestbps": 120,
    "chol": 200, "fbs": 0, "restecg": 0, "thalach": 100,
    "exang": 0, "oldpeak": 1.0, "slope": 1, "ca": 0, "thal": 3
  }'

# View metrics
curl http://localhost:8000/metrics
```

---

## 🏗️ Architecture Overview

```
Client Requests
    ↓
┌─ FastAPI App (8000)
│  ├─ Logging (JSON + Files)
│  ├─ Metrics Collection
│  └─ /metrics endpoint
│
├─→ Prometheus (9090)
│   ├─ Scrapes /metrics
│   ├─ Stores time-series
│   └─ PromQL queries
│
├─→ Grafana (3000)
│   ├─ Queries Prometheus
│   ├─ Dashboard visualization
│   └─ Real-time updates
│
└─→ cAdvisor (8080)
    └─ Container metrics
```

---

## ⚙️ Configuration Files

### Prometheus Configuration
- **Scrape interval**: 15 seconds
- **Evaluation interval**: 15 seconds
- **Jobs**: Prometheus, API, cAdvisor
- **Location**: `monitoring/prometheus.yml`

### Grafana Provisioning
- **Datasources**: Auto-configured to Prometheus
- **Dashboards**: Auto-loaded from JSON
- **Location**: `monitoring/grafana/provisioning/`

### API Configuration
- **Port**: 8000
- **Metrics endpoint**: /metrics
- **Health endpoint**: /health
- **Logging config**: `src/logging_config.py`

---

## 🐳 Docker Compose Services

| Service | Port | Purpose | Health |
|---------|------|---------|--------|
| heart-api | 8000 | API Application | ✓ |
| prometheus | 9090 | Metrics Storage | ✓ |
| grafana | 3000 | Visualization | ✓ |
| cadvisor | 8080 | Container Metrics | ✓ |

---

## 📋 Performance Baselines

| Metric | Expected | Alert |
|--------|----------|-------|
| P95 Latency | < 500ms | > 2000ms |
| Error Rate | < 1% | > 5% |
| Model Success | > 99% | < 95% |
| Throughput | > 10 req/s | < 5 req/s |

---

## 🔧 Common Commands

```bash
# Start monitoring stack
docker-compose up -d

# View service status
docker-compose ps

# Check API health
docker-compose logs heart-api

# View all logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove everything (including volumes)
docker-compose down -v

# Rebuild images
docker-compose up -d --build

# Access logs directory
docker-compose exec heart-api ls -la logs/

# Query Prometheus
curl http://localhost:9090/api/v1/query?query=heart_api_requests_total
```

---

## 📚 Documentation Files

1. **MONITORING_QUICK_REFERENCE.md** - Start here! (Quick commands)
2. **MONITORING.md** - Complete guide (Detailed explanations)
3. **IMPLEMENTATION_SUMMARY.md** - What was implemented
4. **ARCHITECTURE_DIAGRAM.md** - System diagrams
5. **IMPLEMENTATION_CHECKLIST.md** - Verification details

---

## ✨ What Gets Monitored

### API Level
- ✅ Every incoming request (method, path, client IP)
- ✅ Request/response timing
- ✅ Request/response size
- ✅ Response status codes
- ✅ All errors and exceptions

### Model Level
- ✅ Prediction requests
- ✅ Inference time
- ✅ Prediction distribution (at_risk vs no_risk)
- ✅ Confidence scores
- ✅ Model availability

### System Level
- ✅ Container CPU usage
- ✅ Memory usage
- ✅ Disk I/O
- ✅ Network metrics
- ✅ Active processes

### Application Level
- ✅ Request latency distribution
- ✅ Throughput (requests/second)
- ✅ Error rates by type
- ✅ Active connections
- ✅ Cache behavior

---

## 🚨 Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Check port conflicts
lsof -i :8000  # API
lsof -i :9090  # Prometheus
lsof -i :3000  # Grafana

# Free up ports and restart
docker-compose down
docker-compose up -d
```

### Metrics not appearing
```bash
# Wait 1-2 minutes for data to accumulate
# Check if API is receiving traffic
curl http://localhost:8000/health

# Verify metrics endpoint
curl http://localhost:8000/metrics | head -20

# Check Prometheus scraping
# Go to http://localhost:9090/targets
```

### Grafana dashboard empty
```bash
# Check datasource connection
# Settings → Data Sources → Prometheus

# Check dashboard in edit mode
# Look for red errors in panel queries

# Verify Prometheus has data
# http://localhost:9090/graph
# Query: up{job="heart-disease-api"}
```

---

## 💡 Pro Tips

1. **Real-time monitoring**: Keep Grafana dashboard open while testing
2. **Load testing**: Run `bash test_monitoring.sh` to populate metrics
3. **Quick queries**: Use Prometheus at http://localhost:9090 for ad-hoc queries
4. **Log parsing**: Use `jq` for structured JSON log queries
5. **Dashboard customization**: Clone the dashboard and modify queries
6. **Alert setup**: Add alert rules in Prometheus for thresholds
7. **Performance baseline**: Run load test to understand normal behavior

---

## 🎓 Learning Path

1. **Start**: MONITORING_QUICK_REFERENCE.md (5 min)
2. **Learn**: MONITORING.md (20 min)
3. **Understand**: ARCHITECTURE_DIAGRAM.md (10 min)
4. **Implement**: Follow IMPLEMENTATION_SUMMARY.md (reference)
5. **Test**: Run test_monitoring.sh (5 min)
6. **Verify**: Check IMPLEMENTATION_CHECKLIST.md

---

## 📦 Dependencies Added

```
prometheus-client==0.16.0     # Metrics collection
python-json-logger==2.0.4     # JSON logging
structlog==22.1.0             # Structured logging
python-multipart==0.0.5       # Request parsing
```

---

## ✅ Production Checklist

- [x] All services containerized
- [x] Health checks configured
- [x] Data persistence enabled
- [x] Logging configured
- [x] Metrics exposed
- [x] Dashboards created
- [x] Tests passing
- [x] Documentation complete

---

## 🎯 Success Criteria Met

✅ **Logging Integration** - JSON + file-based logging with context
✅ **API Monitoring** - Request/response metrics tracked
✅ **Prometheus** - 15+ metrics collected and exposed
✅ **Grafana** - 10-panel dashboard auto-provisioned
✅ **Visualization** - Real-time monitoring dashboard
✅ **Error Tracking** - Comprehensive error logging
✅ **Documentation** - Complete guides provided
✅ **Testing** - Automated test scripts included

---

## 📞 Support

For issues or questions:
1. Check MONITORING_QUICK_REFERENCE.md for quick answers
2. See MONITORING.md for detailed explanations
3. Review ARCHITECTURE_DIAGRAM.md for system understanding
4. Run test_monitoring.sh to validate setup
5. Check logs: `docker-compose logs -f`

---

## 📝 Summary

This is a **complete, production-grade monitoring and logging solution** that:

- Logs every API request, response, and error
- Tracks 15+ Prometheus metrics
- Visualizes performance with a 10-panel Grafana dashboard
- Provides real-time monitoring and historical analysis
- Follows MLOps best practices
- Is ready for production deployment

**All components are containerized, auto-provisioned, and documented.**

---

**Created**: December 30, 2025
**Status**: ✅ Production Ready
**Documentation**: Complete
**Testing**: Automated scripts included
