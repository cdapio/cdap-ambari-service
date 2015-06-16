import sys
from resource_management import *

class Router(Script):
  def install(self, env):
    print 'Install the CDAP Router';

  def stop(self, env):
    print 'Stop the CDAP Router';

  def start(self, env):
    print 'Start the CDAP Router';

  def status(self, env):
    print 'Status of the CDAP Router';

  def configure(self, env):
    print 'Configure the CDAP Router';

if __name__ == "__main__":
  Router().execute()
