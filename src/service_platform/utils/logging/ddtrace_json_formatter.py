import json
import logging

from ddtrace import tracer


class DdTraceJSONFormatter(logging.Formatter):
    def format(self, record):
        # Create a dictionary from the log record
        log_record = {
            "level": record.levelname,
            "time": self.formatTime(record, self.datefmt),
            "message": record.getMessage(),
            "name": record.name,
            "filename": record.filename,
            "lineno": record.lineno,
        }

        span = tracer.current_span()
        trace_id, span_id = (
            (str((1 << 64) - 1 & span.trace_id), span.span_id) if span else (None, None)
        )

        # add ids to structlog event dictionary
        log_record["dd.trace_id"] = str(trace_id or 0)
        log_record["dd.span_id"] = str(span_id or 0)

        # Convert the dictionary to a JSON string
        return json.dumps(log_record)
