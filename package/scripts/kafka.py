import sys
from resource_management import *

class Kafka(Script):
  def install(self, env):
    print 'Install the CDAP Kafka Server';

  def stop(self, env):
    print 'Stop the CDAP Kafka Server';

  def start(self, env):
    print 'Start the CDAP Kafka Server';

  def status(self, env):
    print 'Status of the CDAP Kafka Server';

  def configure(self, env):
    print 'Configure the CDAP Kafka Server';

if __name__ == "__main__":
  Kafka().execute()
