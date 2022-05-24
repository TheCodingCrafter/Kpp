
# https://stackoverflow.com/questions/20256066/python-split-string-by-spaces-except-when-in-quotes-but-keep-the-quotes/20284563#20284563
def SpaceSplit(string):
  last = 0
  splits = []
  inQuote = None
  for i, letter in enumerate(string):
    if inQuote:
      if (letter == inQuote):
        inQuote = None
    else:
      if (letter == '"' or letter == "'"):
        inQuote = letter

    if not inQuote and letter == ' ':
      splits.append(string[last:i])
      last = i+1

  if last < len(string):
    splits.append(string[last:])

  return splits

class Lexer:
    def __init__(self):
        pass

    def Analyse(self, file):
      tokens = []
      with open(file, 'r') as f:
        for line in f:
          line = line.strip('\n')
          a = SpaceSplit(line)
          c = []
          for x in a:
            if x == '':
              pass
            else:
              c.append(x)
          tokens.append((c, line))
      try:
        del a
      except UnboundLocalError:
        pass
      c = []
      for x in tokens:
        if x == []:
          pass
        else:
          c.append(x)
      return c
