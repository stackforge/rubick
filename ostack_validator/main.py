import sys

from ostack_validator.model_parser import ModelParser
from ostack_validator.inspection import MainConfigValidationInspection

def main(args):
  if len(args) < 1:
    print("Usage: validator <config-snapshot-path>")
    sys.exit(1)

  model_parser = ModelParser()

  model = model_parser.parse(args[0])

  inspections = [MainConfigValidationInspection()]

  results = []
  for inspection in inspections:
    results.extend(inspection.inspect(model))

  for result in results:
    print(result)

if __name__ == '__main__':
  main(sys.argv[1:])

