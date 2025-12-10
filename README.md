DAP4 SCHEMA
-----------


This repository contains the source dap4 schema and it can be used to:

* Understand the scope of DAP4
* Test to validate DMRs (dap4 xml metadata documents)
* Raise issues on the issue tracker

## How to run tests

This repository runs test on github workflows with every Pull Request. It is also possible to run tests locally. Do to so you need the following minimal requirements:

* Python >= 3.11
* lxml>=4.9.3
* pytest>=7.0
* Test .dmr files

Before creating a new pull request, we recommend to run pre-commit locally. pre-commit can be installed as follows:

```
$   pip install pre-commit
$   pre-commit run -a
```

All test dmr files are located in the test directory:

```
$   tests/data/
```

Tests will run to validate any .dmr in the above directory. Therefore to test whether a sample .dmr can be validated against the dap4 schema, simply add the test .dmr file into the above test directory.

To run tests, simply execute:

```
$   pytest -v
```






