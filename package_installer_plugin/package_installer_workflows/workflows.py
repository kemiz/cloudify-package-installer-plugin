__author__ = 'kemi'

from cloudify.decorators import workflow
from cloudify.workflows import ctx
from cloudify.workflows import parameters as p
from package_installer_plugin.constants import *

@workflow
def remove_packages(package, node_id, **_):
    """ uninstalls a specified package from a given node
    :param package: package to uninstall
    :param node_id: node to uninstall package from
    """

    instance = None
    for node in ctx.nodes:
        if node_id == node.id:
            for node_instance in node.instances:
                instance = node_instance
                break
            break

    ctx.logger.info("executing on instance {0}".format(instance))
    operation_path = PACKAGE_COMMANDS + 'remove_packages'
    instance.execute_operation(operation_path, package)


@workflow
def install_packages(package, node_id, **_):
    """ installs a specified package from a given node
    :param package: package to install
    :param node_id: node to install package to
    """

    instance = None
    for node in ctx.nodes:
        if node_id == node.id:
            for node_instance in node.instances:
                instance = node_instance
                break
            break

    ctx.logger.info("executing on instance {0}".format(instance))
    operation_path = PACKAGE_COMMANDS + 'install_packages'
    instance.execute_operation(operation_path, package)