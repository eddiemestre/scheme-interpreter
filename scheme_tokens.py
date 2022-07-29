"""The scheme_tokens module provides functions tokenize_line and tokenize_lines
for converting (iterators producing) strings into (iterators producing) lists
of tokens.  A token may be:

  * A number (represented as an int or float)
  * A boolean (represented as a bool)
  * A symbol (represented as a string)
  * A delimiter, including parentheses, dots, and single quotes

This file also includes some features of Scheme that have not been addressed
in the course, such as quasiquoting and Scheme strings.
"""

from ucb import main
import itertools
import string
import sys
import tokenize

# define global character sets
_NUMERAL_STARTS = set(string.digits) | set('+-.')
_SYMBOL_CHARS = (set('!$%&*/:<=>?@^_~') | set(string.ascii_lowercase) |
                 set(string.ascii_uppercase) | _NUMERAL_STARTS)
_STRING_DELIMS = set('"')
_WHITESPACE = set(' \t\n\r')
_SINGLE_CHAR_TOKENS = set("()'`")
_TOKEN_END = _WHITESPACE | _SINGLE_CHAR_TOKENS | _STRING_DELIMS | {',', ',@'}
DELIMITERS = _SINGLE_CHAR_TOKENS | {'.', ',', ',@'}


def valid_symbol(s):
    """Returns whether s is not a well-formed value."""
    if len(s) == 0:
        return False
    for c in s:
        if c not in _SYMBOL_CHARS:
            return False
    return True

def next_candidate_token(line, k):
    """A tuple (tok, k'), where tok is the next substring of line at or
    after position k that could be a token (assuming it passes a validity
    check), and k' is the position in line following that token.  Returns
    (None, len(line)) when there are no more tokens."""

    while k < len(line):
        c = line[k] # grab the first char in line
        if c == ';': # comment, return None and the size of the line
            return None, len(line)
        elif c in _WHITESPACE: # if c in whitespace, increase k to skip it
            k += 1
        elif c in _SINGLE_CHAR_TOKENS: # if c in this set
            return c, k+1 # return that token and the next val of k (spot in the line)
        elif c == '#':  # Boolean values #t and #f
            return line[k:k+2], min(k+2, len(line)) # return the full boolean value
            # k-k+2 = #f/t
            # the second value is either the length of the line or k+2,
            # whichever is smaller to avoid an error
        elif c == ',': # Unquote; check for @
            if k+1 < len(line) and line[k+1] == '@':
                return ',@', k+2
            return c, k+1 # return unquote and the next val of k
        elif c in _STRING_DELIMS:
            if k+1 < len(line) and line[k+1] == c: # No triple quotes in Scheme
                return c+c, k+2 # double quote
            line_bytes = (bytes(line[k:], encoding='utf-8'),) # Get the rest of the line as bytes
            gen = tokenize.tokenize(iter(line_bytes).__next__) # tokenize the line using python libs
            next(gen) # Throw away encoding token # throw away the first token
            token = next(gen) # grab the next token
            if token.type != tokenize.STRING: # check if the token is string
                raise ValueError("invalid string: {0}".format(token.string))
            return token.string, token.end[1]+k # Return the token as a string through the end of the 
            # Token + the original k
        else: # for all other symbols, NUMERAL_STARTS, SYMBOL_CHARS, TOKEN_END, DELIMITERS
            j = k # create a copy of k in j
             # while j is less than the length of the line and line[j] is not a TOKEN_END char
            while j < len(line) and line[j] not in _TOKEN_END:
                # increase j (build the substring we will eventually grab)
                j += 1
            return line[k:j], min(j, len(line)) # return the substring we created and the position
            # of j now
    return None, len(line)

def tokenize_line(line):
    """The list of Scheme tokens on line.  Excludes comments and whitespace."""
    result = [] # the list of scheme tokens we will be adding to
    # call next candidate token starting at the beginning of the line
    text, i = next_candidate_token(line, 0) 
    # while text (line) is not None
    while text is not None:
        if text in DELIMITERS: # text is either in SINGLE_CHAR_TOKENS or {'.', ',', '@'}
            result.append(text) # append the delimiter
        elif text == '#t' or text.lower() == 'true': # if text is a boolean true
            result.append(True) # append True
        elif text == '#f' or text.lower() == 'false': # if false
            result.append(False) # append false
        elif text == 'nil': # if nil
            result.append(text) # return nil
        elif text[0] in _SYMBOL_CHARS: # if in symbol chars - > number, letter, etc
            number = False # assume number is false
            if text[0] in _NUMERAL_STARTS: # if first char in text is a number or number symbol
                try:
                    result.append(int(text)) # try to append the number
                    number = True # number is true
                except ValueError: # if we can't do it, try to cast as float
                    try:
                        result.append(float(text))
                        number = True
                    except ValueError: # If we still can't, that means its a arithemtic symbol so pass
                        pass
            if not number: # if its not a number 
                if valid_symbol(text): # but is a valid symbol
                    result.append(text.lower()) # append
                else: # or raise a value error
                    raise ValueError("invalid numeral or symbol: {0}".format(text))
        elif text[0] in _STRING_DELIMS: # if the first val in text is a string delim
            result.append(text) # return the whole text
        else: # print warnings otherwise
            print("warning: invalid token: {0}".format(text), file=sys.stderr)
            print("    ", line, file=sys.stderr)
            print(" " * (i+3), "^", file=sys.stderr)
        text, i = next_candidate_token(line, i)
    return result # the list of tokens

def tokenize_lines(input):
    """An iterator that returns lists of tokens, one for each line of the
    iterable input sequence."""
    return map(tokenize_line, input)

def count_tokens(input):
    """Count the number of non-delimiter tokens in input."""
    return len(list(filter(lambda x: x not in DELIMITERS,
                           itertools.chain(*tokenize_lines(input)))))

@main
def run(*args):
    file = sys.stdin
    if args:
        file = open(args[0], 'r')
    print('counted', count_tokens(file), 'non-delimiter tokens')
