#!/bin/sh

while inotifywait -r .; do
    nosetests
done
