__author__ = 'kemi'

# Plugin globals
SERVICE_COMMANDS = 'service.commands.'
PACKAGE_COMMANDS = 'package.commands'

INSTALL = 'install '
REMOVE = 'remove '


# Install commands
APT_GET = 'sudo apt-get -y '
APT_GET_UPDATE = 'sudo apt-get update'
DPKG = 'sudo dpkg -i '
YUM = 'sudo yum -y '
APT_SOURCELIST_DIR = '/etc/apt/sources.list.d/'
YUM_REPOS_DIR = '/etc/yum.repos.d/'

# Services
START_SERVICE_COMMAND = 'sudo service {0} start '
STOP_SERVICE_COMMAND = 'sudo service {0} stop '
RESTART_SERVICE_COMMAND = 'sudo service {0} restart '
