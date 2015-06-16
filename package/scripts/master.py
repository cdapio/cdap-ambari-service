import sys
from resource_management import *

class Master(Script):
  def install(self, env):
    print 'Install the CDAP Master';

  def stop(self, env):
    print 'Stop the CDAP Master';

  def start(self, env):
    print 'Start the CDAP Master';

  def status(self, env):
    print 'Status of the CDAP Master';

  def configure(self, env):
    print 'Configure the CDAP Master';

if __name__ == "__main__":
  Master().execute()
