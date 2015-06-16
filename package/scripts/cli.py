import sys
from resource_management import *

class CLI(Script):
  def install(self, env):
    print 'Install the CDAP CLI';

  def status(self, env):
    print 'Status of the CDAP CLI';

  def configure(self, env):
    print 'Configure the CDAP CLI';

if __name__ == "__main__":
  CLI().execute()
