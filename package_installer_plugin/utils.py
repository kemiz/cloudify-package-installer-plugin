import subprocess
import requests

__author__ = 'kemi'

# Cloudify imports
from cloudify import ctx
from cloudify import exceptions


def run(command):

    command_as_list = command.split()
    ctx.logger.info(command_as_list)
    try:
        execution = subprocess.check_output(command_as_list)
    except Exception as e:
        raise exceptions.NonRecoverableError(
            'Unable to run command. Error: {0}'.format(str(e)))
    finally:
        ctx.logger.info('RAN: {0}. Code: 0.'.format(command))
    return execution


def download_file(source, destination):
    """ Downloads a file from url to destination file """

    ctx.logger.info('Downloading {0} to {1}'.format(source, destination))
    package = requests.get(source, stream=True)
    with open(destination, 'wb') as f:
        for chunk in package.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


def unzip(source, destination):
    ctx.logger.info('Unzipping {0} to {1}'.format(source, destination))
    unzip_command = 'unzip {0} -d {1}'.format(source, destination)
    run(unzip_command)


def move_file(destination, source):
    ctx.logger.info('Moving file "{0}" to "{1}"'.format(source, destination))
    move_command = 'sudo mv {0} {1}'.format(source, destination)
    run(move_command)


def run_maven_command(pom_xml, mvn_operation):
    package_command = 'mvn -f {0} {1}'.format(pom_xml, mvn_operation)
    ctx.logger.info('Executing maven operation: ' + package_command)
    run(package_command)