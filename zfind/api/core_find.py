import os

# Filter files according to inclusion and exclusion rules. These rules follow a pattern similar to multiple grep commands piped together.
# Inclusions and exclusions follow the commutative property. If there are multiple inclusions, each one must match to accept.
# A single matching exclusion means no match.
class Find:

  def __init__(self):
    pass

  def _check_match(self, matcher, matcher_filter_exclude_list, matcher_filter_include_list):

    for matcher_filter_token in matcher_filter_exclude_list:
      token = matcher_filter_token.get_token()
      if token in matcher:
        return False

    if(len(matcher_filter_include_list) == 0):
      return True

    for matcher_filter_token in matcher_filter_include_list:
      token = matcher_filter_token.get_token()
      if token not in matcher:
        return False

    return True

  # Recursively walk through filesystem and either include/exclude files and directories based on user input
  def find(self, scan_dir, file_filter_tokens):

    # Organize the file filter tokens into a map based on file or directory matching and inclusive or exclusive rules
    filter_map = {}
    filter_map["path"] = {}
    filter_map["filename"] = {}
    for key in filter_map:
      filter_map[key]["inclusive"] = []
      filter_map[key]["exclusive"] = []
    for file_filter_token in file_filter_tokens:

      # All filter tokens, 'filename_only' and 'path' are added to the inclusive 'path' check
      if(file_filter_token.is_inclusive()):
        filter_map["path"]["inclusive"].append(file_filter_token)
      if(not file_filter_token.is_filename_only() and not file_filter_token.is_inclusive()):
        filter_map["path"]["exclusive"].append(file_filter_token)

      if(file_filter_token.is_filename_only()):
        if(file_filter_token.is_inclusive()):
          filter_map["filename"]["inclusive"].append(file_filter_token)
        else:
          filter_map["filename"]["exclusive"].append(file_filter_token)

    # Note 'topdown' must be true if excluding directories when using the os.walk function
    for root, dirs, files in os.walk(scan_dir, topdown=True, followlinks=True):

      # Skip the first set of files if we are including specific directories
      for name in files:
        match = self._check_match(name, filter_map["filename"]["exclusive"], filter_map["filename"]["inclusive"])
        if(match):
          match = self._check_match(root + os.path.sep + name, filter_map["path"]["exclusive"], filter_map["path"]["inclusive"])
          if(match):
            yield root + os.path.sep + name

      remove_dirs_index = []
      index = 0;
      for name in dirs:
        path = root + os.path.sep + name
        # First check exclusions only because further checking is not required if the directly is excluded.
        match = self._check_match(path, filter_map["path"]["exclusive"], [])
        if(match):
          # Next check inclusions only, and yield on a match
          match = self._check_match(path, [], filter_map["path"]["inclusive"])
          # Do not output any directories if matching inclusive filenames only
          if(match and len(filter_map["filename"]["inclusive"]) == 0):
            yield root + os.path.sep + name + "/"
        else:
          remove_dirs_index.append(index)
        index = index + 1

      # Note that when removing from the list, it shrinks so the indexes need to be modified by the remove count
      remove_count = 0
      for index in remove_dirs_index:
        del dirs[index - remove_count]
        remove_count = remove_count + 1
