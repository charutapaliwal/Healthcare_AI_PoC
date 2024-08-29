from prometheus_client import start_http_server, Summary, Counter, Gauge

# General Metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
ERROR_COUNT = Counter('error_count', 'Total number of errors')
LAST_PROCESSED_TIME = Gauge('last_processed_time', 'Time when the last request was processed')

# Trustworthy AI Specific Metrics
BIAS_ALERTS = Counter('bias_alerts_count', 'Number of bias alerts triggered')
GUARDRAILS_TRIGGERED = Counter('guardrails_triggered_count', 'Number of times guardrails were triggered')
RED_TEAMING_ALERTS = Counter('red_teaming_alerts_count', 'Number of red teaming alerts detected')
DATA_PRIVACY_ALERTS = Counter('data_privacy_alerts_count', 'Number of data privacy concerns flagged')
REGULATORY_COMPLIANCE_CHECKS = Counter('regulatory_compliance_checks_count', 'Number of regulatory compliance checks')

def start_prometheus_server(port=8000):
    """
    Starts the Prometheus server to expose metrics.

    Parameters:
    port (int): Port on which Prometheus metrics will be exposed.
    """
    start_http_server(port)
    print(f"Prometheus server started on port {port}")

@REQUEST_TIME.time()
def process_request():
    """
    Simulates processing a request. This function would be where you integrate AI-related tasks.
    """
    import random
    import time

    REQUEST_COUNT.inc()  # Increment request count
    try:
        # Simulate request processing time
        time.sleep(random.uniform(0.1, 0.5))
        LAST_PROCESSED_TIME.set_to_current_time()  # Update the gauge with the current time
    except Exception as e:
        ERROR_COUNT.inc()  # Increment error count on failure
        print(f"An error occurred: {e}")

def record_bias_alert():
    BIAS_ALERTS.inc()

def record_guardrail_trigger():
    GUARDRAILS_TRIGGERED.inc()

def record_red_teaming_alert():
    RED_TEAMING_ALERTS.inc()

def record_data_privacy_alert():
    DATA_PRIVACY_ALERTS.inc()

def record_regulatory_compliance_check():
    REGULATORY_COMPLIANCE_CHECKS.inc()

if __name__ == "__main__":
    start_prometheus_server()
    # Simulate some requests
    for _ in range(10):
        process_request()
