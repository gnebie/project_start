import contextvars

# Créer une variable de contexte pour le trace_id
trace_id_var = contextvars.ContextVar("trace_id", default="no-trace-id")
