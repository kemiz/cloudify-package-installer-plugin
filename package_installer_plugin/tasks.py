from cloudify import exceptions, ctx
from cloudify.decorators import operation

__author__ = 'kemi'

# Built in Imports
import platform
import tempfile

# Cloudify Imports
from package_installer_plugin.constants import *
from utils import run, download_file


@operation
def install_packages(config, **_):
    """ Installs a list of packages """

    if config is None:
        config = ctx.node.properties['config']

    ctx.logger.info('Attempting to install packages')
    distro = platform.linux_distribution(full_distribution_name=False)
    distro_lower = [x.lower() for x in distro]
    ctx.logger.info('Working environment: {0} {2} v{1}'.format(distro[0], distro[1], distro[2]))

    ctx.logger.info(config)

    if 'custom_repo' in config:
        _add_custom_repo(config['custom_repo'], distro_lower)

    package_list = config['package_list']

    for package_to_install in package_list:

        # Install from repository (yum / apt)
        if 'http' not in package_to_install:

            ctx.logger.info('Installing from repository: {0}'.format(package_to_install))

            install_command = _get_install_command(
                distro=distro_lower,
                install_from_repo=True,
                package=package_to_install)

            # TODO: apt-get update should not get called every install
            run(APT_GET_UPDATE)

        # Install from package
        else:

            ctx.logger.info('Installing from URL: {0}'.format(package_to_install))
            package = tempfile.mkstemp()
            package_path = package[1]
            download_file(source=package_to_install, destination=package_path)

            install_command = _get_install_command(
                distro=distro_lower,
                install_from_repo=False,
                package=package_path)

        ctx.logger.info('Running command: {0}'.format(install_command))
        run(install_command)


@operation
def remove_packages(config, **_):
    """ removes a package from a given node """

    package_list = config['package_list']

    if 'ubuntu' in platform:
        # TODO: apt-get update should not get called every install
        run(APT_GET_UPDATE)
        remove_command = APT_GET + REMOVE + '{0}'.format(package_list)
    elif 'centos' in platform:
        remove_command = YUM + REMOVE + '{0}'.format(package_list)
    else:
        raise exceptions.NonRecoverableError(
            'Only Centos and Ubuntu supported.')
    run(remove_command)


def _add_keyserver(key_server):
    add_key_server_command = 'sudo apt-key adv --keyserver ' + key_server
    ctx.logger.info('Adding key server: {0}'.format(add_key_server_command))
    run(add_key_server_command)


def _add_source_list(file_path, repo_entry, temp_file):
    ctx.logger.debug('Opening temp file: {0}'.format(temp_file))
    source_list_file = open('/tmp/' + temp_file, "wb")
    ctx.logger.debug('Adding entry to file: {0}'.format(repo_entry))
    source_list_file.write(repo_entry)
    source_list_file.close()
    move_command = 'sudo mv /tmp/' + temp_file + ' ' + file_path + temp_file
    ctx.logger.debug('Moving file to correct location: {0}'.format(move_command))
    run(move_command)


def _add_custom_repo(repo, distro):

    repo_name = repo['name']

    if 'ubuntu' in distro:

        _add_keyserver(repo['apt']['key_server'])

        repo_entry = repo['apt']['entry']
        temp_file = '{0}.list'.format(repo_name)
        file_path = APT_SOURCELIST_DIR

    elif 'centos' in distro:

        repo_entry = repo['yum']['entry']
        temp_file = '{0}.repo'.format(repo_name)
        file_path = YUM_REPOS_DIR

    else:
        raise exceptions.NonRecoverableError(
            'Only CentOS and Ubuntu supported.')

    ctx.logger.info('Adding new repository source: {0}'.format(repo_name))
    _add_source_list(file_path, repo_entry, temp_file)


def _get_install_command(distro, install_from_repo, package):
    if 'ubuntu' in distro:
        if install_from_repo:
            install_command = APT_GET + INSTALL + '{0}'.format(package)
        else:
            install_command = DPKG + '{0}'.format(package)
        ctx.logger.info('Installing on Ubuntu: ' + install_command)
    elif 'centos' in distro:
        if install_from_repo:
            install_command = YUM + INSTALL + package
        else:
            install_command = YUM + INSTALL + '{0}'.format(package)
        ctx.logger.info('Installing on CentOS: ' + install_command)
    else:
        raise exceptions.NonRecoverableError(
            'Only CentOS and Ubuntu supported.')

    return install_command
