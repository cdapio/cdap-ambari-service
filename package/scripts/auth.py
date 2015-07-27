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
    import status_params
    env.set_params(params)
    self.configure(env)
    daemon_cmd = format('/opt/cdap/security/bin/svc-auth-server start')
    no_op_test = format('ls {status_params.cdap_auth_pid_file} >/dev/null 2>&1 && ps -p $(<{status_params.cdap_auth_pid_file}) >/dev/null 2>&1')
    Execute( daemon_cmd,
             user=params.cdap_user,
             not_if=no_op_test
    )

  def stop(self, env):
    print 'Stop the CDAP Auth Server'
    import params
    self.configure(env)
    Execute('service cdap-auth-server stop')

  def status(self, env):
    import status_params
    Execute('ls ' + status_params.cdap_auth_pid_file + ' >/dev/null 2>&1 && ps -p $(<' + status_params.cdap_auth_pid_file + ') >/dev/null 2>&1')

  def configure(self, env):
    print 'Configure the CDAP Auth Server'
    import params
    env.set_params(params)
    helpers.cdap_config('auth')

if __name__ == "__main__":
  Auth().execute()
