import sys
from resource_management import *

class CLI(Script):
  def install(self, env):
    print 'Install the CDAP CLI'
    import params
    # Add repository file
    helpers.add_repo(params.files_dir + params.repo_file, params.os_repo_dir)
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
