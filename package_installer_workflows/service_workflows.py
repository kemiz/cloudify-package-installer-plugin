__author__ = 'kemi'

from cloudify.decorators import workflow
from cloudify.workflows import ctx
from cloudify.workflows import parameters
from package_installer_plugin.constants import *


@workflow
def start_service(**_):

    """ Starts a service on a given node """
    ctx.logger.info("Starting service...")

    for node in ctx.nodes:
        if node.id == parameters.service_name:
            for node_instance in node.instances:
                ctx.logger.info("Starting service {0}".format(node_instance))
                plugin_operation_path = SERVICE_COMMANDS + 'start_service'
                node_instance.execute_operation(plugin_operation_path, kwargs={'service_name': parameters.service_name})


@workflow
def stop_service(**_):

    """ stops a service on a given node """
    ctx.logger.info("Stopping service...")

    for node in ctx.nodes:
        if node.id == parameters.service_name:
            for node_instance in node.instances:
                ctx.logger.info("Stopping service {0}".format(node_instance))
                plugin_operation_path = SERVICE_COMMANDS + 'stop_service'
                node_instance.execute_operation(plugin_operation_path, kwargs={'service_name': parameters.service_name})