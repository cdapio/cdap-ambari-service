import sys
from resource_management import *

class Auth(Script):
  def install(self, env):
    print 'Install the CDAP Auth Server';

  def stop(self, env):
    print 'Stop the CDAP Auth Server';

  def start(self, env):
    print 'Start the CDAP Auth Server';

  def status(self, env):
    print 'Status of the CDAP Auth Server';

  def configure(self, env):
    print 'Configure the CDAP Auth Server';

if __name__ == "__main__":
  Auth().execute()
