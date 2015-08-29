__author__ = 'kemi'

from cloudify.decorators import workflow
from cloudify.workflows import ctx
from cloudify.workflows import parameters as p
from package_installer_plugin.constants import *


@workflow
def start_service(service_name, node_id, **_):
    """
    Starts a service on a given node
    :param service_name: name of service to start
    :param node_id: node to start the service on
    """

    instance = None
    for node in ctx.nodes:
        if node_id == node.id:
            for node_instance in node.instances:
                instance = node_instance
                break
            break

    ctx.logger.info("executing instance {0}".format(instance))
    plugin_operation_path = SERVICE_COMMANDS + 'start_service'
    instance.execute_operation(plugin_operation_path, service_name)