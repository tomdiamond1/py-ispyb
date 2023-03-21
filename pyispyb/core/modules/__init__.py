"""
Project: py-ispyb.

https://github.com/ispyb/py-ispyb

This file is part of py-ispyb software.

py-ispyb is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

py-ispyb is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with py-ispyb. If not, see <http://www.gnu.org/licenses/>.
"""


__license__ = "LGPLv3+"


import os
from importlib import import_module

from ...config import settings


def init_app(app, **kwargs):
    """Init modules."""
    module_list = settings.module
    for module_plugin in module_list:
        for module_name in module_plugin:
            enabled = module_plugin[module_name]["ENABLED"]
            if enabled:
                module_name: str = module_plugin[module_name]["MODULE_NAME"]
                module = import_module(".%s" % module_name[:-3], package=__name__)
                if hasattr(module, "init_app"):
                    module.init_app(app, **kwargs)
