## Cloudify Package Installer Plugin

This plugin allows you to install & remove a list of packages on a provisioned host.
It also provides hooks to the standard linux service commands to control the operation of an installed service.

### Plugin Operations
#### Install Operation
The install operation accepts a configuration that specifies what packages dependencies need to be installed and any custom repositories or source-lists that need to be added.
- <b>`config`</b> : <br>
  - <b>`custom_repo`</b>: a `dict` contains information for adding a custom repository or source-list.<br> 
  - <b>`package_list`</b>: a list of packages to be installed. These can be names of packages that can be obtained from either `yum` or `apt` repositories. The list may also contain `URL` locations of packages that the plugin can download and install.<br><br> 
Below is an example configuration that installs MongoDB through the standard repository by adding a custom sourcelist before obtaining the files:<br><br>

  ```yaml
  config:
    custom_repo:
      name: 'mongodb-org-3.0'
      # The definition of the new repository we want to add, both for yum & apt
      # In this case we are configuring for MongoDB
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

#### Start / Stop Service Operations

The `start_service` and `stop_service` operations uses the provided `service_name` property to execute:
  ```bash
  service <MY_SERVICE> start / stop
  ```  
<br>
This can also be passed as a parameter if it needs overriding.
<br>

### Workflows 

The plugin comes with built-in workflows to install, remove, reinstall and upgrade packages as well as controlling the operation of installed services post deployment.
<br><br>

### Extending the ServiceInstaller base-type

It is intended that you extend the ServiceInstaller in order to provide further tailored service types definitions. For example to create a deploy a new `Elasticsearch` instance you can define a new type:

```yaml
  cloudify.nodes.Elasticsearch:
    derived_from: cloudify.nodes.ServiceInstaller
    properties:
      service_name:
        default: 'elasticsearch'
      version:
        default: '1.7.1'
      config:
        default:
          package_list:
            # Install Java
            - 'openjdk-7-jdk'
            # Install Elasticsearch from URL
            - 'https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.1.noarch.rpm'
```

Then we can easily specify a simple node template as:

```yaml
  # The service instance
  elasticsearch:
    type: cloudify.nodes.Elasticsearch
    relationships:
      - type: cloudify.relationships.contained_in
        target: elasticsearch_host
  
  # The VM host node
  elasticsearch_host:
    type: monitoredhosts.openstack.nodes.MonitoredServer
```
This would then provision and deploy a new Elasticsearch node on OpenStack.<br>
Currently the plugin does not support custom startup configurations for any services installed.
<br><br>
### Usage

You can find here an [example blueprint]("https://github.com/kemiz/package-installer-example-cfy3") demonstrating the use of this plugin.
