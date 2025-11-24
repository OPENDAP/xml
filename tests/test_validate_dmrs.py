from lxml import etree
import pytest
from pathlib import Path

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
def test_validate_dmr_files(dap4_schema, dmr_file):
    """Validate all DMR/XML files in the dmr/ directory."""
    with open(dmr_file, "rb") as f:
        doc = etree.parse(f)
    try:
        dap4_schema.assertValid(doc)
    except etree.DocumentInvalid as e:
        pytest.fail(f"DMR validation failed for {dmr_file}:\n{str(e)}")
