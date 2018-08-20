#!/bin/sh

MAIN="com.thaiopensource.relaxng.util.Driver"
CP="lib/jing.jar:build/dap4-datatypes.jar"

# java -cp "$CP" $MAIN -i dap4.rng test1.xml

# Usage validate-dap4 <grammar> <xml to validate>
#       validate-dap4 <xml to validate>

if test -z "$2"
then
    grammar=../dap/dap4.rng
    xml=$1
else
    grammar=$1
    xml=$2
fi
    
java -cp "$CP" $MAIN -i $grammar $xml