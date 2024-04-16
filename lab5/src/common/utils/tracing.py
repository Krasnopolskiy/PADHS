from opentelemetry.trace import Tracer


def observed(tracer: Tracer):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(func.__qualname__):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def aobserved(tracer: Tracer):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(func.__qualname__):
                return await func(*args, **kwargs)

        return wrapper

    return decorator
