import sys
import ambari_helpers as helpers
from resource_management import *

class Auth(Script):
  def install(self, env):
    print 'Install the CDAP Auth Server'
    import params
    self.configure(env)
    # Add repository file
    helpers.add_repo(params.files_dir + params.repo_file, params.os_repo_dir)
    # Install any global packages
    self.install_packages(env)
    # Install package
    helpers.package('cdap-security')

  def start(self, env):
    print 'Start the CDAP Auth Server'
    import params
    self.configure(env)
    Execute('service cdap-auth-server start')

  def stop(self, env):
    print 'Stop the CDAP Auth Server'
    import params
    self.configure(env)
    Execute('service cdap-auth-server stop')

  def status(self, env):
    print 'Status of the CDAP Auth Server'
    import params
    self.configure(env)
    Execute('service cdap-auth-server status')

  def configure(self, env):
    print 'Configure the CDAP Auth Server'
    import params
    helpers.cdap_config

if __name__ == "__main__":
  Auth().execute()
