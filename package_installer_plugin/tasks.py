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
def install(package_list, install_from_repo, **_):
    """ Installs a list of packages """

    ctx.logger.info('Attempting to install packages')
    distro = platform.linux_distribution(full_distribution_name=False)
    distro_lower = [x.lower() for x in distro]
    ctx.logger.info('Working environment: {0} {2} v{1}'.format(distro[0], distro[1], distro[2]))

    # Install from repository (yum / apt)
    if install_from_repo:
        for package_to_install in package_list:
            ctx.logger.info('Installing from repository: {0}'.format(package_to_install))
            _install_from_repo(package=package_to_install, platform=distro_lower)

    # Install from package
    else:
        for package_to_install in package_list:
            ctx.logger.info('Installing from URL: {0}'.format(package_to_install))
            _install_from_repo(package=package_to_install, platform=distro_lower)


def _install_from_repo(platform, package):
    """ installs a package from repository """

    # Install package
    if 'ubuntu' in platform:
        # TODO: apt-get update should not get called every install
        run('sudo apt-get update')
        install_command = 'sudo apt-get -qq --no-upgrade install {0}'.format(package)
    elif 'centos' in platform:
        install_command = 'sudo yum -y -q install {0}'.format(package)
    else:
        raise exceptions.NonRecoverableError(
            'Only Centos and Ubuntu supported.')

    run(install_command)


def _install_from_url(platform, package_url):
    """ installs a package from repository """

    # Download package
    _, package_file = tempfile.mkstemp()

    # Install package
    if 'ubuntu' in platform:
        install_command = 'sudo dpkg -i {0}'.format(package_file)
    elif 'centos' in platform:
        install_command = 'sudo yum install -y {0}'.format(package_file)
    else:
        raise exceptions.NonRecoverableError(
            'Only Centos and Ubuntu supported.')

    _download_package(package_file, package_url)

    run(install_command)


def _download_package(package_file, url):
    """ Downloads package from url to tempfile """

    ctx.logger.debug('Downloading: {0}'.format(url))
    package = requests.get(url, stream=True)

    with open(package_file, 'wb') as f:
        for chunk in package.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
