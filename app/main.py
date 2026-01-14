import structlog
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
# IMPORT THE MISSING PIECE
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.routes import router as leave_router

# --- CONFIGURATION TO WRITE TO FILES ---

# 1. Setup Logging (Write to app_logs.json)
log_file = open("app_logs.json", "a")
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(file=log_file)
)
logger = structlog.get_logger()

# 2. Setup Tracing (Write to app_traces.json)
trace_file = open("app_traces.json", "a")
trace.set_tracer_provider(TracerProvider())

# We use the ConsoleExporter but direct it to our file
# We force flush=True to ensure data is written immediately
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter(out=trace_file))
)

# --- APP SETUP ---
app = FastAPI(title="Employee Leave API")

# 3. Setup Prometheus Metrics
Instrumentator().instrument(app).expose(app)

# 4. ENABLE AUTOMATIC TRACING (The missing link)
FastAPIInstrumentor.instrument_app(app)

app.include_router(leave_router)

@app.on_event("startup")
async def startup():
    logger.info("application_startup", status="ready")

@app.get("/health")
def health_check():
    logger.info("health_check_accessed")
    return {"status": "ok"}