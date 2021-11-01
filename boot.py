from zfind.run.runner import Runner

class Boot:

  def __init__(self):
    pass;

  def boot(self):

    runner = Runner()
    runner.run()

if __name__ == "__main__":
  boot = Boot()
  boot.boot()
