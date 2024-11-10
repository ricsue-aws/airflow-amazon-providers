# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

import logging
from importlib import import_module

from airflow.configuration import conf
from airflow.exceptions import AirflowException

log = logging.getLogger(__name__)


def init_xframe_protection(app):
    """
    Add X-Frame-Options header.

    Use it to avoid click-jacking attacks, by ensuring that their content is not embedded into other sites.

    See also: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
    """
    x_frame_enabled = conf.getboolean("webserver", "X_FRAME_ENABLED", fallback=True)
    if x_frame_enabled:
        return

    def apply_caching(response):
        response.headers["X-Frame-Options"] = "DENY"
        return response

    app.after_request(apply_caching)


def init_api_auth(app):
    """Load authentication backends."""
    auth_backends = conf.get("api", "auth_backends")

    app.api_auth = []
    try:
        for backend in auth_backends.split(","):
            auth = import_module(backend.strip())
            auth.init_app(app)
            app.api_auth.append(auth)
    except ImportError as err:
        log.critical("Cannot import %s for API authentication due to: %s", backend, err)
        raise AirflowException(err)


def init_cache_control(app):
    def apply_cache_control(response):
        if "Cache-Control" not in response.headers:
            response.headers["Cache-Control"] = "no-store"
        return response

    app.after_request(apply_cache_control)