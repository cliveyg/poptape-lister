import os.path
import json
from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import ValidationError as JsonValidationError

def assert_valid_schema(data, schema_type):
    # checks whether the given data matches the schema

    if schema_type == 'uuid':
        schema = _load_json_schema('schemas/uuid.json')
    elif schema_type == 'bulk_uuids':
        schema = _load_json_schema('schemas/bulk_uuids.json')

    return validate(data, schema, format_checker=draft7_format_checker)


def _load_json_schema(filename):
    # loads the given schema file
    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath) as schema_file:
        return json.loads(schema_file.read())
