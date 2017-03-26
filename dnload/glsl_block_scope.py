from dnload.glsl_block import GlslBlock
from dnload.glsl_block import extract_tokens
from dnload.glsl_block_assignment import glsl_parse_assignment
from dnload.glsl_block_call import glsl_parse_call
from dnload.glsl_block_control import glsl_parse_control
from dnload.glsl_block_declaration import glsl_parse_declaration
from dnload.glsl_block_return import glsl_parse_return

########################################
# GlslBlockScope #######################
########################################
 
class GlslBlockScope(GlslBlock):
  """Scope block."""

  def __init__(self, lst, explicit):
    """Constructor."""
    GlslBlock.__init__(self)
    self.__explicit = explicit
    # Hierarchy.
    self.addChildren(lst)

  def format(self, force):
    """Return formatted output."""
    ret = "".join(map(lambda x: x.format(force), self._children))
    if self.__explicit or (1 < len(self._children)):
      return "{%s}" % (ret)
    return ret

  def __str__(self):
    """String representation."""
    return "Scope(%u)" % (len(self._children))

########################################
# Functions ############################
########################################

def glsl_parse_content(source):
  """Parse generic content."""
  # Nested scopes without extra content make no sense.
  if 2 <= len(source) and ("{" == source[0].format(False)) and ("}" == source[-1].format(False)):
    return glsl_parse_content(source[1:-1])
  # Loop over content.
  ret = []
  while source:
    (block, remaining) = glsl_parse_scope(source)
    if block:
      ret += [block]
      source = remaining
      continue
    (block, remaining) = glsl_parse_control(source)
    if block:
      ret += [block]
      source = remaining
      continue
    (block, remaining) = glsl_parse_declaration(source)
    if block:
      ret += [block]
      source = remaining
      continue
    (block, remaining) = glsl_parse_assignment(source)
    if block:
      ret += [block]
      source = remaining
      continue
    (block, remaining) = glsl_parse_call(source)
    if block:
      ret += [block]
      source = remaining
      continue
    (block, remaining) = glsl_parse_return(source)
    if block:
      ret += [block]
      source = remaining
      continue
    raise RuntimeError("cannot parse content: %s" % (str(map(str, source))))
  return ret

def glsl_parse_scope(source, explicit = True):
  """Parse scope block."""
  (content, remaining) = extract_tokens(source, ("?{",))
  if not (content is None):
    return (GlslBlockScope(glsl_parse_content(content), explicit), remaining)
  # If explicit scope is not expected, try one-statement scope.
  elif not explicit:
    (assignment, remaining) = glsl_parse_assignment(source)
    if assignment:
      return (GlslBlockScope([assignment], explicit), remaining)
  # No scope found.
  return (None, source)

def is_glsl_block_scope(op):
  """Tell if given object is GlslBlockScope."""
  return isinstance(op, GlslBlockScope)
