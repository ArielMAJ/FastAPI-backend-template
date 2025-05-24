import contextvars
import time
from uuid import uuid4

from fastapi import Request, Response
from fastapi.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

from src.configs.envs import Config

REQUEST_UUID = contextvars.ContextVar("request_uuid", default=None)


class LoggerMiddleware(BaseHTTPMiddleware):
    UNABLE_TO_READ_BODY = b"<unable to read body>"
    BODY_IGNORED = b"<body ignored>"

    def __init__(
        self,
        app,
        logger,
    ):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        uuid = uuid4()
        REQUEST_UUID.set(uuid)

        if self._should_log_input_body(request):
            try:
                body = await request.body()
            except Exception:
                body = self.UNABLE_TO_READ_BODY
        else:
            body = self.BODY_IGNORED

        self.logger.warning(
            f"Start request path={request.url.path}; method={request.method}; "
            f"{body=};"
        )
        start_time = time.time()

        response: Response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)

        if self._should_ignore_method_and_path(
            request.method,
            request.url.path,
            Config.LOGGER_IGNORE_PATHS,
        ):
            self.logger.warning(
                f"Request completed in {formatted_process_time}ms; "
                f"Status Code={response.status_code};"
            )
            return response

        res_body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(res_body))
        res_body_decoded = (
            res_body[0].decode()
            if self._should_log_output_body(request, res_body)
            else self.BODY_IGNORED
        )

        self.logger.warning(
            f"Request completed in {formatted_process_time}ms; "
            f"Status Code={response.status_code}; body={res_body_decoded};"
        )
        return response

    def _should_log_output_body(self, request: Request, res_body):
        return res_body and not self._should_ignore_method_and_path(
            request.method,
            request.url.path,
            Config.LOGGER_IGNORE_OUTPUT_BODY_PATHS,
        )

    def _should_log_input_body(self, request: Request):
        return not self._should_ignore_method_and_path(
            request.method,
            request.url.path,
            Config.LOGGER_IGNORE_INPUT_BODY_PATHS,
        )

    def _should_ignore_method_and_path(
        self, method, path, to_ignore_methods_and_paths_tuple
    ):
        return (method, path) in to_ignore_methods_and_paths_tuple
