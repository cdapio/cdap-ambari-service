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
    self.configure(env)
    Execute('mkdir -p ' + params.kafka_log_dir)
    Execute('service cdap-kafka-server start')

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
    helpers.cdap_config

if __name__ == "__main__":
  Kafka().execute()
