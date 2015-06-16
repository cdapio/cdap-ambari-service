import sys
from resource_management import *

class UI(Script):
  def install(self, env):
    print 'Install the CDAP UI';

  def stop(self, env):
    print 'Stop the CDAP UI';

  def start(self, env):
    print 'Start the CDAP UI';

  def status(self, env):
    print 'Status of the CDAP UI';

  def configure(self, env):
    print 'Configure the CDAP UI';

if __name__ == "__main__":
  UI().execute()
