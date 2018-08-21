#!/bin/sh
#
# Usage ./validate-dap4.sh <file>
#
# You must build the dap4-datatypes library for this validator to work. Go to
# dap4-datatypes and run ant to do that.

MAIN="com.thaiopensource.relaxng.util.Driver"
CP="dap4-datatypes/jing.jar:dap4-datatypes/build/dap4-datatypes.jar"

java -cp $CP $MAIN -i dap4.rng $1
