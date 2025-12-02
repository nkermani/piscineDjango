#!/bin/sh

if [ "$#" -ne 1 ]; then
	echo "Usage: $0 <bitly-url>"
	exit 1
fi

curl -sI "$1" | grep -i 'Location:' | cut -d' ' -f2
