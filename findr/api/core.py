from refactorr.api.checker import Checker
from refactorr.api.transform import Transform

class Refactor:

  def __init__(self):
    pass;

  # Scans files and finds flexible matching patterns to the search tokens.
  def scan(self, filepath, find_tokens):

    checkers = []

    try:
      with open(filepath, "r") as input_file:
        while True:
          base_checker = Checker(find_tokens)
          checkers.append(base_checker)

          char = input_file.read(1)
          if not char:
            break

          matched_checkers = []
          for checker in checkers:
            match = checker.check_next(char)
            if(match):
              if(checker.is_done()):
                yield checker.get_record()
              else:
                matched_checkers.append(checker)
          checkers = matched_checkers
            
        # If the file terminates, add one empty string to all checkers
        for checker in checkers:
          match = checker.check_next("")
          if(checker.is_done()):
            yield checker.get_record()
    except UnicodeDecodeError:
      print("[WARNING] could not decode: " + filepath + " as utf-8, skipping refactor.")

  # Deterimines the case of a token given the prior casing and the next char
  # Cases are either 'upper', 'lower', 'title', or 'none' and if not set Python's None
  def resolve_case(self, current_case, next_char):
    if(current_case is "none"):
      return current_case

    if(current_case is None):
      if(next_char.isupper()):
        return "title"
      else:
        return "lower"
    else:
      if(next_char.isupper()):
        if(current_case == "title"):
          return "upper"
        elif(current_case == "lower"):
          return "none"
        return current_case
      else:
        if(current_case == "title" or current_case == "lower"):
          return current_case
        else:
          return "none"

  # Outputs a list of operations to apply to replace tokens
  def classify(self, raw_text, find_tokens):

    transform = Transform()

    case = None
    delimiter = ""

    find_tokens_index = 0
    char_index = 0

    first_raw = False
    for char in raw_text:

      if(first_raw):
        if(char.isalnum()):
          delimiter = ""
          transform.push(case, delimiter)
          if(char.isupper()):
            case = "title"
          else:
            case = "lower"
          char_index = char_index + 1
        else:
          delimiter = char
          transform.push(case, delimiter)
          case = None
        # Reset default values
        delimiter = ""
        first_raw = False
        continue


      case = self.resolve_case(case, char)
      
      if(char.lower() != find_tokens[find_tokens_index][char_index]):
        raise "Classification error"

      char_index = char_index + 1
      first_raw = False

      if(char_index == len(find_tokens[find_tokens_index])):
        find_tokens_index = find_tokens_index + 1
        char_index = 0
        first_raw = True

    # The last token always has a null delimiter.
    delimiter = ""
    transform.push(case, delimiter)

    return transform

  #def transform_replacement(self, transform, replace_tokens):
  #  pass

  # Computes replacements for the search tokens attempting to follow similar casing and stylistic rules
  def compute(self, raw_text, find_tokens, replace_tokens):
  
    transform = self.classify(raw_text, find_tokens)
    #print("Transforms for [" + raw_text + "] are " + str(transform))
    replacement_text = transform.apply(replace_tokens)
    print("Replacements: " + raw_text + " -> " + replacement_text)

  def run(self):
    print("refactor - hi")
