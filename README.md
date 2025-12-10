DAP4 SCHEMA
-----------


This repository contains the source dap4 schema and it can be used to:

* Understand the scope of DAP4
* Test to validate DMRs (dap4 xml metadata documents)
* Raise issues on the issue tracker

## How to run tests

This repository runs tests on github workflows with every Pull Request. It is also possible to run tests locally. To do so you will need to have Python >=3.11 and install the following (minimal) required python dependencies:

* lxml>=4.9.3
* pytest>=7.0

You can install python packages via pip 
```
$   pip install <package>
```
or a package manager such as miniforge conda, pixi, etc. 

You will also need test dmr files to validate against. All test dmr files are located in the following test directory.


```
$   tests/data/
```

To run the tests execute the following command

```
$   pytest -v
```

Tests will run and attempt to validate any .dmr in the above `tests/data/` directory. Thus to test whether a sample `.dmr` can be validated against the dap4 schema, simply add the test `.dmr` file into the above test directory.


## How to contribute
You can contribute by raising issues, with a short and clear description of the problem, the expected behavior, and include an example so that the issue/error can be reproduced.

The issue will help us improve the dap4 schema if needed, or add a test that highlights the improper behavior.

If a change is needed, create branch of the project, make a change to the spec, and include a test dmr that highlights the new behavior. 

Before creating a new pull request, always make sure tests pass locally and we recommend to run pre-commit locally for basic formatting. `pre-commit` can be installed as follows:

```
$   pip install pre-commit
$   pre-commit run -a
```







