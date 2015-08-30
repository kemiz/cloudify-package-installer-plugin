## Cloudify Package Installer Plugin

This plugin allows you to install a given list of packages on a provisioned host.

The plugin implements 2 Cloudify `@operation`s to install & remoe packages.

#### Install Operation

- <b>`config`</b> - The install operation accepts a configuration `dict` that specifies what packages dependencies need to be installed and any custom repositories or source-lists that need to be added.<br>
  - <b>`custom_repo`</b>: a `dict` contains information for adding a custom repository or source-list.<br> 
  - <b>`package_list`</b>: a list of packages to be installed. These can be names of packages that can be obtained from either `yum` or `apt` repositories. The list may also contain `URL` locations of packages that the plugin can download and install.<br><br> 
Below is an example configuration that installs MongoDB through the standard repository by adding a custom sourcelist before obtaining the files.

  ```config:
      custom_repo:
        name: 'mongodb-org-3.0'
        # The definition of the new repository we want to add, both for yum & apt, in this case for MongoDB
        yum:
          name: 'mongodb-org-3.0'
          entry: '[mongodb-org-3.0]
                  name=MongoDB Repository
                  baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.0/x86_64/
                  gpgcheck=0
                  enabled=1'
        apt:
          key_server: 'hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10'
          entry: 'deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse'
      # The list of packages to install using apt or yum
      package_list:
        - 'mongodb-org'
  ```

### Usage

You can find here an [example blueprint]("https://github.com/kemiz/package-installer-example-cfy3") demonstrating the use of this plugin.
