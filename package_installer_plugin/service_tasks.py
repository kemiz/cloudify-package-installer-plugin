__author__ = 'kemi'

# Cloudify Imports
from package_installer_plugin.constants import *
from utils import run
from cloudify import ctx
from cloudify.decorators import operation


@operation
def start_service(**_):
    service_name = ctx.node.properties['service_name']
    start_command = START_SERVICE_COMMAND + service_name
    ctx.logger.info('Starting service: ' + service_name)
    ctx.logger.info('Running command: {0}'.format(start_command))
    run(start_command)


@operation
def stop_service(**_):
    service_name = ctx.node.properties['service_name']
    stop_command = STOP_SERVICE_COMMAND + service_name
    ctx.logger.info('Stopping service: ' + service_name)
    ctx.logger.info('Running command: {0}'.format(stop_command))
    run(stop_command)


@operation
def restart_service(**_):
    service_name = ctx.node.properties['service_name']
    stop_command = RESTART_SERVICE_COMMAND + service_name
    ctx.logger.info('Restarting service: ' + service_name)
    ctx.logger.info('Running command: {0}'.format(stop_command))
    run(stop_command)