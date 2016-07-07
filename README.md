# Ambari CDAP Services

This is currently a work in progress and does not support all features of CDAP. New features
are added to the `develop` branch and are released along with new CDAP major/minor versions
using a release branch.

This has been tested on Ambari 2.0, 2.1, and 2.2 as shipped by Hortonworks and has been tested
on HDP 2.2, 2.3, and 2.4 for most functionality. Certain functions are dependent on the version
of Ambari in use.

## Installation

This software is meant to be installed using the native package management tools in Linux. After
building the packages, install the appropriate package on your Ambari server and restart Ambari
to make CDAP an available service.

### Building from source

Simply checkout the repository and run `./build.sh` to build the RPM and DEB packages. This
will check out the CDAP service using the latest release of CDAP. Specific major/minor releases
of CDAP can be obtained by pulling the corresponding branch. For example, for CDAP 3.0, you would
checkout the `release/3.0` branch.

## License

   Copyright © 2015-2016 Cask Data, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
software except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions
and limitations under the License.
