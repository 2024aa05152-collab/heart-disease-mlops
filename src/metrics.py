"""
Prometheus metrics collection for Heart Disease Prediction API
Provides comprehensive monitoring of API performance and model predictions
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
import time
from typing import Callable
from functools import wraps


# ============================================================================
# API Performance Metrics
# ============================================================================

# Request counter
request_count = Counter(
    'heart_api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status']
)

# Request latency histogram
request_latency = Histogram(
    'heart_api_request_duration_seconds',
    'API request latency in seconds',
    ['method', 'endpoint'],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0)
)

# Request size histogram
request_size = Histogram(
    'heart_api_request_size_bytes',
    'API request size in bytes',
    ['method', 'endpoint'],
    buckets=(100, 500, 1000, 5000, 10000, 50000)
)

# Response size histogram
response_size = Histogram(
    'heart_api_response_size_bytes',
    'API response size in bytes',
    ['method', 'endpoint'],
    buckets=(100, 500, 1000, 5000, 10000)
)

# ============================================================================
# Model Performance Metrics
# ============================================================================

# Prediction counter
prediction_count = Counter(
    'heart_model_predictions_total',
    'Total number of predictions made',
    ['model_status']  # success, error
)

# Prediction latency
prediction_latency = Histogram(
    'heart_model_prediction_duration_seconds',
    'Model prediction latency in seconds',
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5)
)

# Risk prediction distribution
risk_distribution = Counter(
    'heart_disease_predictions',
    'Distribution of heart disease predictions',
    ['risk_category']  # no_risk, at_risk
)

# Average probability gauge
avg_probability = Gauge(
    'heart_disease_average_probability',
    'Average probability of heart disease across recent predictions'
)

# ============================================================================
# Error Metrics
# ============================================================================

# Error counter
error_count = Counter(
    'heart_api_errors_total',
    'Total number of API errors',
    ['error_type']  # validation_error, model_error, server_error
)

# ============================================================================
# System Metrics
# ============================================================================

# Active requests gauge
active_requests = Gauge(
    'heart_api_active_requests',
    'Current number of active API requests'
)

# Model loading status
model_loaded = Gauge(
    'heart_model_loaded',
    'Whether the model is successfully loaded (1=yes, 0=no)'
)


# ============================================================================
# Utility Functions
# ============================================================================

def track_api_call(method: str, endpoint: str):
    """
    Decorator to track API call metrics
    
    Args:
        method: HTTP method
        endpoint: API endpoint path
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            active_requests.inc()
            
            try:
                result = func(*args, **kwargs)
                status = "success"
                duration = time.time() - start_time
                request_latency.labels(method=method, endpoint=endpoint).observe(duration)
                request_count.labels(method=method, endpoint=endpoint, status=status).inc()
                return result
            except Exception as e:
                status = "error"
                error_count.labels(error_type=type(e).__name__).inc()
                request_count.labels(method=method, endpoint=endpoint, status=status).inc()
                duration = time.time() - start_time
                request_latency.labels(method=method, endpoint=endpoint).observe(duration)
                raise
            finally:
                active_requests.dec()
        
        return wrapper
    return decorator


def track_prediction(func: Callable):
    """
    Decorator to track model prediction metrics
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            prediction_latency.observe(duration)
            prediction_count.labels(model_status="success").inc()
            return result
        except Exception as e:
            prediction_count.labels(model_status="error").inc()
            duration = time.time() - start_time
            prediction_latency.observe(duration)
            raise
    
    return wrapper


def update_risk_distribution(prediction: int, probability: float):
    """
    Update risk prediction distribution and average probability
    
    Args:
        prediction: Prediction result (0 or 1)
        probability: Probability value
    """
    risk_category = "at_risk" if prediction == 1 else "no_risk"
    risk_distribution.labels(risk_category=risk_category).inc()
    avg_probability.set(probability)


def set_model_loaded(status: bool):
    """
    Set model loading status
    
    Args:
        status: True if model is loaded successfully
    """
    model_loaded.set(1 if status else 0)
