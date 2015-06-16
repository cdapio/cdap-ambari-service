import sys
import ambari_helpers as helpers
from resource_management import *

class UI(Script):
  def install(self, env):
    print 'Install the CDAP UI';
    import params
    self.configure(env)
    # Add repository file
    helpers.add_repo(params.files_dir + params.repo_file, params.os_repo_dir)
    # Install any global packages
    self.install_packages(env)
    # Install package
    helpers.package('cdap-ui')

  def stop(self, env):
    print 'Stop the CDAP UI';

  def start(self, env):
    print 'Start the CDAP UI';

  def status(self, env):
    print 'Status of the CDAP UI';

  def configure(self, env):
    print 'Configure the CDAP UI';

if __name__ == "__main__":
  UI().execute()
