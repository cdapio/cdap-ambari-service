import sys
import ambari_helpers as helpers
from resource_management import *

class Kafka(Script):
  def install(self, env):
    print 'Install the CDAP Kafka Server'
    import params
    self.configure(env)
    # Add repository file
    helpers.add_repo(params.files_dir + params.repo_file, params.os_repo_dir)
    # Install any global packages
    self.install_packages(env)
    # Install package
    helpers.package('cdap-kafka')

  def start(self, env):
    print 'Start the CDAP Kafka Server'
    import params
    env.set_params(params)
    self.configure(env)
    daemon_cmd = format('/opt/cdap/kafka/bin/svc-kafka-server start')
    no_op_test = format('ls {params.cdap_kafka_pid_file} >/dev/null 2>&1 && ps -p $(<{params.cdap_kafka_pid_file}) >/dev/null 2>&1')
    Execute( daemon_cmd,
             user=params.cdap_user,
             not_if=no_op_test
    )

  def stop(self, env):
    print 'Stop the CDAP Kafka Server'
    import params
    self.configure(env)
    Execute('service cdap-kafka-server stop')

  def status(self, env):
    print 'Status of the CDAP Kafka Server'
    import params
    self.configure(env)
    Execute('service cdap-kafka-server status')

  def configure(self, env):
    print 'Configure the CDAP Kafka Server'
    import params
    env.set_params(params)
    helpers.cdap_config('kafka')

    Directory( params.kafka_log_dir,
        owner = params.cdap_user,
        group = params.user_group,
        recursive = True
    )

if __name__ == "__main__":
  Kafka().execute()
