#!/bin/sh

a=0

while [ $a -lt 3 ]
do
    python test.py & wait
    a = `expr $a + 1`
done