from lxml import etree

DAP4_NS = "http://xml.opendap.org/ns/DAP/4.0#"
NS = {"d": DAP4_NS}

BASE_TYPES = {
    "Byte",
    "SignedByte",
    "Int16",
    "UInt16",
    "Int32",
    "UInt32",
    "Int64",
    "UInt64",
    "Float32",
    "Float64",
    "String",
    "Url",
    "Opaque",
    "Structure",
}


DAP4_NS = "http://xml.opendap.org/ns/DAP/4.0#"
NS = {"d": DAP4_NS}

BASE_TYPES = {
    "Byte",
    "SignedByte",
    "Int16",
    "UInt16",
    "Int32",
    "UInt32",
    "Int64",
    "UInt64",
    "Float32",
    "Float64",
    "String",
    "Url",
    "Opaque",
    "Structure",
}


def validate_dim_semantics(doc):
    """
    Enforce: Every <Dim> inside BaseTypes must have (name or size),
    and cannot omit both.
    """
    root = doc.getroot()

    for tag in BASE_TYPES:
        for base in root.xpath(f"//d:{tag}", namespaces=NS):
            dims = base.xpath(".//d:Dim", namespaces=NS)

            for dim in dims:
                name = dim.get("name")
                size = dim.get("size")

                # must have one or the other
                if name is None and size is None:
                    raise ValueError(
                        f"<Dim> in base type <{tag}> must have either @name or @size: "
                        f"{etree.tostring(dim, encoding='UTF-8')}"
                    )
