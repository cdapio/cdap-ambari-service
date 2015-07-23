import sys
import ambari_helpers as helpers
from resource_management import *

class Router(Script):
  def install(self, env):
    print 'Install the CDAP Router'
    import params
    self.configure(env)
    # Add repository file
    helpers.add_repo(params.files_dir + params.repo_file, params.os_repo_dir)
    # Install any global packages
    self.install_packages(env)
    # Install package
    helpers.package('cdap-gateway')

  def start(self, env):
    print 'Start the CDAP Router'
    import params
    env.set_params(params)
    self.configure(env)
    daemon_cmd = format('/opt/cdap/gateway/bin/svc-router start')
    no_op_test = format('ls {params.cdap_router_pid_file} >/dev/null 2>&1 && ps -p $(<{params.cdap_router_pid_file}) >/dev/null 2>&1')
    Execute( daemon_cmd,
             user=params.cdap_user,
             not_if=no_op_test
    )

  def stop(self, env):
    print 'Stop the CDAP Router'
    import params
    self.configure(env)
    Execute('service cdap-router stop')

  def status(self, env):
    print 'Status of the CDAP Router'
    import params
    self.configure(env)
    Execute('service cdap-router status')

  def configure(self, env):
    print 'Configure the CDAP Router'
    import params
    env.set_params(params)
    helpers.cdap_config('router')

if __name__ == "__main__":
  Router().execute()
