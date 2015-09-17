__author__ = 'kemi'

from cloudify.decorators import workflow
from cloudify.workflows import ctx
from cloudify.workflows import parameters
from package_installer_plugin.constants import *

@workflow
def remove_packages(**_):
    """ uninstalls a specified package from a given node """

    for node in ctx.nodes:
        for node_instance in node.instances:
            if node_instance.id == parameters.node_id:
                ctx.logger.info("executing on instance {0}".format(node_instance))
                operation_path = PACKAGE_COMMANDS + 'remove_packages'
                node_instance.execute_operation(operation_path, kwargs={'config': {parameters.config}})


@workflow
def install_packages(**_):

    """ installs a specified package from a given node """

    for node in ctx.nodes:
        for node_instance in node.instances:
            if node_instance.id == parameters.node_id:
                ctx.logger.info("executing on instance {0}".format(node_instance))
                operation_path = PACKAGE_COMMANDS + 'install_packages'
                node_instance.execute_operation(operation_path, kwargs={'config': {parameters.config}})