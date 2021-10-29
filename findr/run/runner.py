from findr.api.core_find import Find
from findr.input.loader import Loader
import logging

class Runner:

  def __init__(self):
    pass;

  def run(self):

    loader = Loader()
    loader.run()
    file_filter_tokens = loader.get_file_filter_tokens()
    for file_filter_token in file_filter_tokens:
      logging.debug("File filter token: " + str(file_filter_token))
      

    find = Find()
    file_matches = find.find(".", file_filter_tokens)

    for file_match in file_matches:
      print(file_match)

def main():
  runner = Runner()
  runner.run()
