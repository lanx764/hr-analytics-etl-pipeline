class PipelineError(Exception):
    pass

class APIError(PipelineError):
    pass

class ValidationError(PipelineError):
    pass

class TransformError(PipelineError):
    pass