__author__ = 'kemi'

# Built in Imports
import requests
import platform
import tempfile

# Cloudify Imports
from package_installer_plugin.constants import *
from utils import run
from cloudify import ctx
from cloudify import exceptions
from cloudify.decorators import operation


@operation
def install_packages(package_list, **_):
    """ Installs a list of packages """

    ctx.logger.info('Attempting to install packages')
    distro = platform.linux_distribution(full_distribution_name=False)
    distro_lower = [x.lower() for x in distro]
    ctx.logger.info('Working environment: {0} {2} v{1}'.format(distro[0], distro[1], distro[2]))

    for package_to_install in package_list:
        # Install from repository (yum / apt)
        if 'http' not in package_to_install:
            ctx.logger.info('Installing from repository: {0}'.format(package_to_install))

            install_command = _get_install_command(
                distro=distro_lower,
                install_from_repo=True,
                package=package_to_install)

            # TODO: apt-get update should not get called every install
            run(APT_UPDATE_COMMAND)

        # Install from package
        else:
            ctx.logger.info('Installing from URL: {0}'.format(package_to_install))

            _, package_file = tempfile.mkstemp()
            _download_package(package_file, package_to_install)

            install_command = _get_install_command(
                distro=distro_lower,
                install_from_repo=False,
                package=package_to_install)

        ctx.logger.info('Running command: {0}'.format(install_command))
        run(install_command)


def _get_install_command(distro, install_from_repo, package):
    if 'ubuntu' in distro:
        if install_from_repo:
            install_command = APT_COMMAND + INSTALL + '{0}'.format(package)
        else:
            install_command = DPKG_COMMAND + '{0}'.format(package)
        ctx.logger.info('Installing on Ubuntu: ' + install_command)
    elif 'centos' in distro:
        if install_from_repo:
            install_command = YUM_COMMAND + INSTALL + '{0}'.format(package)
        else:
            install_command = YUM_COMMAND + INSTALL + '{0}'.format(package)
        ctx.logger.info('Installing on CentOS: ' + install_command)
    else:
        raise exceptions.NonRecoverableError(
            'Only CentOS and Ubuntu supported.')

    return install_command


def _download_package(package_file, url):
    """ Downloads package from url to tempfile """

    ctx.logger.debug('Downloading: {0}'.format(url))
    package = requests.get(url, stream=True)

    with open(package_file, 'wb') as f:
        for chunk in package.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


@operation
def remove_package(package_list, **kwargs):
    """ removes a package from a given node """

    if 'ubuntu' in platform:
        # TODO: apt-get update should not get called every install
        run(APT_UPDATE_COMMAND)
        remove_command = APT_COMMAND + REMOVE + '{0}'.format(package_list)
    elif 'centos' in platform:
        remove_command = YUM_COMMAND + REMOVE + '{0}'.format(package_list)
    else:
        raise exceptions.NonRecoverableError(
            'Only Centos and Ubuntu supported.')
    run(remove_command)