#!/usr/bin/env python3

import connexion
import logging
from logging.handlers import RotatingFileHandler
from logs import encoder
from .config import Config
import os
from fluent import sender
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


NAME = "Logs-Service"

def configure_monitoring(app, config):

    resource = Resource(attributes={"service.name": NAME})

    fluent_bit_host = config['monitoring']['fluent_bit_host']
    fluent_bit_port = config['monitoring']['fluent_bit_port']
    fluent_bit_sender = sender.FluentSender('Logs-Service', host=fluent_bit_host, port=fluent_bit_port)
    propagator = TraceContextTextMapPropagator()

    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
    exporter = OTLPSpanExporter(endpoint=f"http://{config['monitoring']['opentelemetry_url']}:{config['monitoring']['opentelemetry_port']}", insecure=True)
    span_processor = BatchSpanProcessor(
        exporter,
        max_queue_size=config['monitoring']['opentelemetry_max_queue_size'],
        schedule_delay_millis=config['monitoring']['opentelemetry_schedule_delay_millis'],
        max_export_batch_size=config['monitoring']['opentelemetry_max_export_batch_size'],
        export_timeout_millis=config['monitoring']['opentelemetry_export_timeout_millis'],
    )

    trace.get_tracer_provider().add_span_processor(span_processor)

    FlaskInstrumentor().instrument_app(app)

    class FluentBitHandler(logging.Handler):

        def __init__(self):
            logging.Handler.__init__(self)

        def emit(self, record):
            log_entry = self.format(record)
            log_data = {
                'message': log_entry,
                'level': record.levelname,
                'timestamp': record.created,
                'logger': record.name,
                'function': record.funcName,
                'line': record.lineno,
                'container_name': os.environ.get('CONTAINER_NAME', ''),
            }

            # # Obtener el trace ID actual
            current_context = trace.get_current_span().get_span_context()

            trace_id = current_context.trace_id
            traceparent_id = current_context.span_id
            log_data['traceID'] = hex(trace_id)[2:]
            if traceparent_id != None:
                log_data['traceparent'] = hex(traceparent_id)[2:]
            fluent_bit_sender.emit('Logs-Service', log_data)

    loggers = [app.logger, ]
    for l in loggers:
         l.addHandler(FluentBitHandler())


def configure_logging(app):
    del app.logger.handlers[:]
    loggers = [app.logger, ]
    handlers = []
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(verbose_formatter())
    file_handler = RotatingFileHandler(filename="service_logs.log", maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(verbose_formatter())
    handlers.append(console_handler)
    handlers.append(file_handler)
   
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def verbose_formatter():
    return logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "function": "%(funcName)s", "line": %(lineno)d, "message": %(message)s}',
        datefmt='%d/%m/%Y %H:%M:%S'
    )


app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'CAPIF_Auditing_API'},
            pythonic_params=True)

configure_logging(app.app)

config = Config()
if eval(os.environ.get("MONITORING").lower().capitalize()):
    configure_monitoring(app.app, config.get_config())

if __name__ == '__main__':
    app.run(port=8080)
