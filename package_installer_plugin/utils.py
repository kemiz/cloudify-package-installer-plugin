import subprocess
import requests

__author__ = 'kemi'

# Cloudify imports
from cloudify import ctx
from cloudify import exceptions


def run(command):

    command_as_list = command.split()
    execution = None
    output = None

    try:
        execution = subprocess.check_output(command_as_list)
    except Exception as e:
        raise exceptions.NonRecoverableError(
            'Unable to run command. Error {0}'.format(execution.returncode))
    finally:
        if execution.returncode != 0:
            raise exceptions.RecoverableError(
                'Unable to run command. Error: {0}'.format(execution))
        ctx.logger.info(
            'RAN: {0}. OUT: {1}. Code: {2}.'.format(
                command, output, execution.returncode))
    return execution


def download_package(package_file, url):
    """ Downloads package from url to tempfile """

    ctx.logger.debug('Downloading: {0}'.format(url))
    package = requests.get(url, stream=True)

    with open(package_file, 'wb') as f:
        for chunk in package.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


def unzip(source, destination):
    ctx.logger.info('Unzipping file: ' + source)
    unzip_command = 'unzip {0} -d {1}'.format(source, destination)
    run(unzip_command)