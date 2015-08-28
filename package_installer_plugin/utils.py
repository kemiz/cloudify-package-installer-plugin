__author__ = 'kemi'

# Built in imports
from subprocess import Popen, PIPE

# Cloudify imports
from cloudify import ctx
from cloudify import exceptions


def run(command):

    command_as_list = command.split()
    execution = None
    output = None

    try:
        execution = Popen(command_as_list, stdout=PIPE)
        output = execution.communicate()[0]
        execution.wait()
    except Exception as e:
        raise exceptions.NonRecoverableError(
            'Unable to run command. Error {0}'.format(str(e)))
    finally:
        ctx.logger.info(
            'RAN: {0}. OUT: {1}. Code: {2}.'.format(
                command, output, execution.returncode))

    return execution
