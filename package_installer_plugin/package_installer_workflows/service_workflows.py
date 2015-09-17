__author__ = 'kemi'

from cloudify.decorators import workflow
from cloudify.workflows import ctx
from cloudify.workflows import parameters
from package_installer_plugin.constants import *


@workflow
def start_service(**_):

    """ Starts a service on a given node """

    for node in ctx.nodes:
        for node_instance in node.instances:
            ctx.logger.info("executing instance {0}".format(node_instance))
            plugin_operation_path = SERVICE_COMMANDS + 'start_service'
            node_instance.execute_operation(plugin_operation_path, parameters.service_name)