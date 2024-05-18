from typing import Any, List

def get_closes(objects: List[Any]) -> List[float]:
  return [*map(lambda ob: ob['c'], objects)]
