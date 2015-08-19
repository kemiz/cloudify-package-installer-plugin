##Cloudify Package Installer Plugin

This plugin allows you to install a given list of packages on a provisioned host.

The plugin implements Cloudify `@operation` (`Install`) that takes in 2 parameters: <br>

- `package_list` - a `dict` of packages to be installed. This can be a list of packages that can be obtained either from `yum` or `apt` repositories. This may also be a list or `URLs` referencing packages that need to be downloaded and installed.<br><br>
- `install_from_repo` - a `boolean` on whether or not the list is a list of `URLs` or repository packages. **Note: It is intended that in the future this will be removed and a mixed list may be provided**

### Usage

You can find here an [example blueprint]("https://github.com/kemiz/package-installer-example-cfy3") demonstrating the use of this plugin.
