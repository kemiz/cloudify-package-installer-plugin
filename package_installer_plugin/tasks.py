########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

# Built in Imports
import requests
import platform
import tempfile

# Cloudify Imports
from utils import run
from cloudify import ctx
from cloudify import exceptions
from cloudify.decorators import operation


@operation
def install(service_to_install, **_):
    """ Installs a list of packages """

    ctx.logger.info('Installing {0}'.format(service_to_install))
    distro = platform.linux_distribution(full_distribution_name=False)
    distro_lower = [x.lower() for x in distro]
    ctx.logger.info('Working environment: {0} {2} v{1}'.format(distro[0], distro[1], distro[2]))

    if service_to_install is 'elasticsearch':
        from elasticsearch_plugin import tasks as elasticsearch
        elasticsearch.install(install_java=True)

    elif service_to_install is 'logstash':
        from logstash_plugin import tasks as logstash
        logstash.install()