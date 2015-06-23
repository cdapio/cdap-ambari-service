import sys
from resource_management import *

class CLI(Script):
  def install(self, env):
    print 'Install the CDAP CLI'

  def configure(self, env):
    print 'Configure the CDAP CLI'
    import params
    helpers.cdap_config('client')

  def status(self, env):
    raise ClientComponentHasNoStatus()

if __name__ == "__main__":
  CLI().execute()
