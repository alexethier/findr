import sys
import logging
from findr.api.file_filter_token import FilterToken




# Project specific wrapper around argparse
class Loader:

  def __init__(self):
    self._file_filter_tokens = []

  def print_arg_error(self, bad_arg):
    print("Error: Unknown input argument: " + bad_arg)

  def print_help(self):
    print("Usage: [-g INCLUSIVE_MATCH ] ")
    print("       [-ge EXCLUSIVE_MATCH ] ")

  def run(self):

    # Setup logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.WARN)

    input_key = None
    index = 1
    for index in range(1, len(sys.argv)):
      arg = sys.argv[index]

      if(input_key != None):
        parsed = self._load_file_filter_token(input_key, arg)
        if(not parsed):
          self.print_arg_error(sys.argv[index -1])
          self.print_help()
          return False
        else:
          input_key = None
      elif(arg.startswith('-g')):
        input_key = arg[2:]
      elif(arg.startswith('--g')):
        input_key = arg[3:]
      elif(arg == '-h' or arg == '--help'):
        self.print_help()
        return False
      # Must check '-vv' before '-v'
      elif(arg.startswith('-vv')):
        logging.getLogger().setLevel(logging.DEBUG)
      elif(arg.startswith('-v')):
        logging.getLogger().setLevel(logging.INFO)
      else:
        self.print_arg_error(arg)
        self.print_help()
        return False
      
    if(input_key is not None):
      print("Error: match token must follow expression '" + sys.argv[index] + "'")
      self.print_help()
      return False

    return True
    
    #log_info = args.v
    #if(log_info):
    #  logging.getLogger().setLevel(logging.INFO)
    #log_debug = args.vv
    #if(log_debug):
    #  logging.getLogger().setLevel(logging.DEBUG)
    #logging.debug("Debug logging enabled.")

    ## Loop through unknown arguments, if any start with '-g' or '--g' the following unknown argument will 
    #input_key = None
    #for unknown_arg in unknown_arguments:
    #  if(input_key != None):
    #    parsed = self._load_file_filter_token(input_key, unknown_arg)
    #    if(not parsed):
    #      parser.parse_args()
    #      break
    #    input_key = None
    #  elif(unknown_arg.startswith('-g')):
    #    input_key = unknown_arg[2:]
    #  elif(unknown_arg.startswith('--g')):
    #    input_key = unknown_arg[3:]
    #  else:
    #    parser.parse_args()
    #    break

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
