import sys
import ambari_helpers as helpers
from resource_management import *

class Master(Script):
  def install(self, env):
    print 'Install the CDAP Master'
    import params
    self.configure(env)
    # Add repository file
    helpers.add_repo(params.files_dir + params.repo_file, params.os_repo_dir)
    # Install any global packages
    self.install_packages(env)
    # Install package
    helpers.package('cdap-master')

  def start(self, env):
    print 'Start the CDAP Master'
    import params
    self.configure(env)
    helpers.create_hdfs_dir(params.hdfs_namespace, params.hdfs_user, 755)
    # Hack to work around CDAP-1967
    self.remove_jackson
    Execute('service cdap-master start')

  def stop(self, env):
    print 'Stop the CDAP Master'
    import params
    self.configure(env)
    Execute('service cdap-master stop')

  def status(self, env):
    print 'Status of the CDAP Master'
    import params
    self.configure(env)
    Execute('service cdap-master status')

  def configure(self, env):
    print 'Configure the CDAP Master'
    import params
    env.set_params(params)
    helpers.cdap_config('master')

  def remove_jackson(self):
    Execute('rm -f /opt/cdap/master/lib/org.codehaus.jackson.jackson-*')

if __name__ == "__main__":
  Master().execute()
