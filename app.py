from flask import Flask
import time

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

resource = Resource.create({"service.name": "demo-flask-service"})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

tracer = trace.get_tracer(__name__)

@app.route("/")
def home():
    with tracer.start_as_current_span("custom-home-span"):
        time.sleep(0.2)
        return "Hello from Jaeger tracing demo!"

@app.route("/db")
def fake_db():
    with tracer.start_as_current_span("fake-db-call"):
        time.sleep(0.5)
        return "Fake DB call completed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
