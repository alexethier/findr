import argparse
import logging
from findr.api.file_filter_token import FilterToken

# Project specific wrapper around argparse
class Loader:

  def __init__(self):
    self._file_filter_tokens = []

  def run(self):

    parser = argparse.ArgumentParser(description='Refactor tokens in a project.')
    parser.add_argument('-v', action='store_true', help='Output INFO logging.')
    parser.add_argument('-vv', action='store_true', help='Output DEBUG logging.')
    #parser.add_argument('file_filter', metavar='file_filter', type=str, nargs='*',
    #                    help='Filter which files to refactor')
    #parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                    const=sum, default=max,
    #                    help='sum the integers (default: find the max)')
    
    args, unknown_arguments = parser.parse_known_args()

    # Setup logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.WARN)
    
    log_info = args.v
    if(log_info):
      logging.getLogger().setLevel(logging.INFO)
    log_debug = args.vv
    if(log_debug):
      logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Debug logging enabled.")

    input_key = None
    for unknown_arg in unknown_arguments:
      if(input_key != None):
        parsed = self._load_file_filter_token(input_key, unknown_arg)
        if(not parsed):
          parser.parse_args()
          break
        input_key = None
      elif(unknown_arg.startswith('-g')):
        input_key = unknown_arg[2:]
      elif(unknown_arg.startswith('--g')):
        input_key = unknown_arg[3:]
      else:
        parser.parse_args()
        break

  def _load_file_filter_token(self, input_key, token):
    input_chars = [char for char in input_key]

    inclusive = True
    regex = False
    filename_only = False

    for char in input_chars:
      if(char == "e"):
        inclusive = False
      elif(char == "r"):
        raise "TODO: Support regex"
        regex = True
      elif(char == "f"):
        filename_only = True
      else:
        return False

    filter_token = FilterToken(token, inclusive, regex, filename_only)
    self._file_filter_tokens.append(filter_token)
    return True

  def get_file_filter_tokens(self):
    return self._file_filter_tokens
