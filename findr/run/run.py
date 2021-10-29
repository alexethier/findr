from refactorr.api.core import Refactor
from refactorr.find.findr import Findr
from refactorr.input.loader import Loader
import logging

class Runner:

  def __init__(self):
    pass;

  def run(self):
    print("Running!")

    loader = Loader()
    loader.run()
    file_filter_tokens = loader.get_file_filter_tokens()
    for file_filter_token in file_filter_tokens:
      logging.debug("File filter token: " + str(file_filter_token))
      

    findr = Findr()
    file_matches = findr.find(".", file_filter_tokens)

    find_tokens = loader.get_find_tokens()
    replace_tokens = loader.get_replace_tokens()

    print("FIND TOKENS: " + str(find_tokens))
    print("REPLACE TOKENS: " + str(replace_tokens))

    refactor = Refactor()
    for file_match in file_matches:
      logging.info("Found file: " + file_match)

      if not file_match.endswith('/'):
        find_token_matches = refactor.scan(file_match, find_tokens)
        for find_token_match in find_token_matches:
          refactor.compute(find_token_match, find_tokens, replace_tokens)
