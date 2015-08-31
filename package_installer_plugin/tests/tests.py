__author__ = 'kemi'

import os
import unittest

from cloudify.workflows import local


class TestPlugin(unittest.TestCase):

    def setUp(self):
        # build blueprint path
        blueprint_path = os.path.join(os.path.dirname(__file__),
                                      'blueprint', 'blueprint.yaml')

        # inject input from test
        inputs = {
            'test_input': 'new_test_input'
        }

        # setup local workflow execution environment
        self.env = local.init_env(blueprint_path,
                                  name=self._testMethodName,
                                  inputs=inputs)

    def test_my_task(self):

        # execute install workflow
        self.env.execute('install', task_retries=0)

        # extract single node instance
        instance = self.env.storage.get_node_instances()[0]

        # assert runtime properties is properly set in node instance
        self.assertEqual(instance.runtime_properties['value_of_some_property'],
                         'new_test_input')

        # assert deployment outputs are ok
        self.assertDictEqual(self.env.outputs(),
                             {'test_output': 'new_test_input'})