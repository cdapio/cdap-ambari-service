import sys
import ambari_helpers as helpers
from resource_management import *

class UI(Script):
  def install(self, env):
    print 'Install the CDAP UI'
    import params
    self.configure(env)
    # Add repository file
    helpers.add_repo(params.files_dir + params.repo_file, params.os_repo_dir)
    # Install any global packages
    self.install_packages(env)
    # Install package
    helpers.package('cdap-ui')
    # TODO: make sure this is available
    helpers.package('nodejs')

  def start(self, env):
    print 'Start the CDAP UI'
    import params
    import status_params
    env.set_params(params)
    self.configure(env)
    daemon_cmd = format('/opt/cdap/ui/bin/svc-ui start')
    no_op_test = format('ls {status_params.cdap_ui_pid_file} >/dev/null 2>&1 && ps -p $(<{status_params.cdap_ui_pid_file}) >/dev/null 2>&1')
    Execute( daemon_cmd,
             user=params.cdap_user,
             not_if=no_op_test
    )

  def stop(self, env):
    print 'Stop the CDAP UI'
    import params
    self.configure(env)
    Execute('service cdap-ui stop')

  def status(self, env):
    import status_params
    check_process_status(status_params.cdap_ui_pid_file)

  def configure(self, env):
    print 'Configure the CDAP UI'
    import params
    env.set_params(params)
    helpers.cdap_config('ui')

if __name__ == "__main__":
  UI().execute()
