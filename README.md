# Ambari CDAP Services

This project is an Ambari service definition for [CDAP](http://cask.co/products/cdap/).

This has been tested on Ambari 2.2, 2.3, and 2.4 as shipped by Hortonworks and has been tested
on HDP 2.2, 2.3, 2.4, and 2.5 for most functionality. Certain functions are dependent on the version
of Ambari in use, such as Quick Links, which is only supported in Ambari 2.4+ for custom services.

New features are added to the `develop` branch and are released along with new CDAP major/minor
versions using a release branch. Bug fixes and security features are backported.

## Installation

This software is intended to be installed using the native package management tools in Linux. After
building the packages, install the appropriate package on your Ambari server and restart Ambari
to make CDAP an available service.

### Building from Source

Simply checkout the repository and run `./build.sh` to build the RPM and DEB packages. This
will check out the CDAP service using the latest release of CDAP. Specific major/minor releases
of CDAP can be obtained by pulling the corresponding branch. For example, for CDAP 4.3, you would
checkout the `release/4.3` branch.

### Installing packages

#### Debian/Ubuntu

```
sudo dpkg -i ./cdap-ambari-service*.deb
sudo ambari-server restart
```

#### RHEL/CentOS/etc

```
sudo yum localinstall ./cdap-ambari-service*.rpm
sudo ambari-server restart
```

## License

   Copyright © 2015-2017 Cask Data, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
software except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions
and limitations under the License.
