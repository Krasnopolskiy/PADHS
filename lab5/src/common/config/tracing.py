from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.aio_pika import AioPikaInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def instrument():
    FastAPIInstrumentor().instrument()
    AioPikaInstrumentor().instrument()


class TracingConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    tempo_url: str = Field(alias="TEMPO_URL")

    def setup_tracing(self, attributes: dict):
        provider = TracerProvider(
            resource=Resource(attributes=attributes),
        )
        processor = BatchSpanProcessor(
            span_exporter=OTLPSpanExporter(endpoint=self.tempo_url),
        )
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        instrument()
