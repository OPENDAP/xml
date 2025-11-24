from lxml import etree
import pytest
from pathlib import Path
from validate_dmr_semantics import validate_dim_semantics

# Path to this test file
TEST_DIR = Path(__file__).resolve().parent

# Path to project root
ROOT_DIR = TEST_DIR.parent
# Path to the schema
SCHEMA_PATH = ROOT_DIR / "dap4" / "dap4.xsd"
# Path to test dmrs
DATA_DIR = TEST_DIR / "data"
DMR_PATHS = list(DATA_DIR.glob("*.dmr"))


@pytest.fixture(scope="session")
def dap4_schema():
    """Load and compile the DAP4 XML schema."""
    with open(SCHEMA_PATH, "rb") as f:
        schema_doc = etree.parse(f)
    return etree.XMLSchema(schema_doc)


@pytest.mark.parametrize("dmr_file", DMR_PATHS)
def test_valid_dmrs(dap4_schema, dmr_file):
    if not dmr_file.name.startswith("Invalid"):
        doc = etree.parse(str(dmr_file))
        # XSD validation
        dap4_schema.assertValid(doc)
        # Semantic validation
        validate_dim_semantics(doc)


def test_fail_validate_dim_BaseType(dap4_schema):
    dmr_file = DATA_DIR / "Invalid_BaseType_Dim.dmr"

    if dmr_file.name.startswith("Invalid"):
        doc = etree.parse(str(dmr_file))
        # XSD validation
        dap4_schema.assertValid(doc)
        with pytest.raises(ValueError):
            validate_dim_semantics(doc)
