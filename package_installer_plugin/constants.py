__author__ = 'kemi'

# Plugin globals
service_commands = 'service.commands.'
package_commands = 'package.commands'

install = 'install '
remove = 'remove '
install_packages = 'install_packages'
remove_packages = 'remove_packages'


# Install commands
apt_get = 'sudo apt-get -y '
apt_get_update = 'sudo apt-get update'
dpkg = 'sudo dpkg -i '
yum = 'sudo yum -y '


# Services
START_SERVICE_COMMAND = 'sudo start service '
STOP_SERVICE_COMMAND = 'sudo stop service '
RESTART_SERVICE_COMMAND = 'sudo restart service '
