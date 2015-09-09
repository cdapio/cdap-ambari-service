# Copyright © 2015 Cask Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

import sys
import ambari_helpers as helpers
from resource_management import *


class CLI(Script):
    def install(self, env):
        print 'Install the CDAP CLI'
        import params
        # Add repository file
        helpers.add_repo(
            params.files_dir + params.repo_file,
            params.os_repo_dir
        )
        # Install any global packages
        self.install_packages(env)
        # Install package
        helpers.package('cdap-cli')
        self.configure(env)

    def configure(self, env):
        print 'Configure the CDAP CLI'
        import params
        env.set_params(params)
        helpers.cdap_config('cli')

    def status(self, env):
        raise ClientComponentHasNoStatus()

if __name__ == "__main__":
    CLI().execute()
