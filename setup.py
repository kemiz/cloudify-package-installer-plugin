from setuptools import setup

setup(
    name='cloudify-package-installer-plugin',
    version='1.2.1',
    author='kemiz',
    packages=['package_installer_plugin'],
    license='LICENSE',
    install_requires=[
        "cloudify-plugins-common==3.2.1",
        "requests",
        'cloudify'
    ]
)
