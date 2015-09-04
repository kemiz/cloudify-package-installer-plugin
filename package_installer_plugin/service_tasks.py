__author__ = 'kemi'

# Cloudify Imports
from package_installer_plugin.constants import *
from utils import run
from cloudify import ctx
from cloudify.decorators import operation


@operation
def start_service(service_name, **_):
    start_command = RESTART_SERVICE_COMMAND.format(service_name)
    ctx.logger.info('Starting service: ' + service_name)
    ctx.logger.info('Running command: {0}'.format(start_command))
    run(start_command)


@operation
def stop_service(service_name, **_):
    stop_command = STOP_SERVICE_COMMAND.format(service_name)
    ctx.logger.info('Stopping service: ' + service_name)
    ctx.logger.info('Running command: {0}'.format(stop_command))
    run(stop_command)


@operation
def restart_service(service_name, **_):
    restart_command = RESTART_SERVICE_COMMAND.format(service_name)
    ctx.logger.info('Restarting service: ' + service_name)
    ctx.logger.info('Running command: {0}'.format(restart_command))
    run(restart_command)