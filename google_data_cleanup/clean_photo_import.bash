#!/bin/bash

fullpath=${1:-.}

( cd "$fullpath";
  find  . -mindepth 2 -type f -exec mv {} .. \;
  find . -type d -empty -delete
)
