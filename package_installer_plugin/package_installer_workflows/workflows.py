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
    plugin_operation_path = INSTALLER_PLUGIN + INSTALL_TASKS + REMOVE_PACKAGES
    instance.execute_operation(plugin_operation_path, package)


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
    plugin_operation_path = INSTALLER_PLUGIN + INSTALL_TASKS + INSTALL_PACKAGES
    instance.execute_operation(plugin_operation_path, package)