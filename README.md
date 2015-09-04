# Ambari CDAP Services

This is currently a work in progress.

It has been tested with Ambari 2.0 and HDP 2.2 release.

## Installation

Simply check out the repository on your Ambari server as described and restart Ambari. This
will check out the CDAP service using the latest release of CDAP. Specific versions of CDAP
can be gotten by pulling the corresponding branch. For example, for CDAP 3.1, you would
checkout the `release/3.1` branch.

```
git clone https://github.com/caskdata/ambari-cdap-stack.git /var/lib/ambari-server/resources/stacks/HDP/2.2/services/CDAP
git checkout release/3.1 # Optional
ambari-server restart
```

## License

   Copyright © 2015 Cask Data, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
software except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions
and limitations under the License.
