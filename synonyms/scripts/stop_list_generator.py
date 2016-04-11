#!/bin/env python3
from __future__ import with_statement

__author__ = 'veselt12'
import argparse
import sys

def count(word,l):
    return sum(list(map(lambda w: int(word in w),l)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('input_file', type=str, help='One word per line')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    args = parser.parse_args()
    words=set()
    with open(args.input_file) as file:
        for word in file:
            word=word.strip().lower()
            words.add(word)
    words=list(words)     
    blacklisted=set()
    
    try:
        while True:
            w=input("Enter search term: ")
            w=w.lower().strip()
            y=input("Currently there is %d of matched words, do you want to edit search term? (y/N): " % count(w,words))
            if y.lower().strip() == 'y':
                continue
            blacklisted.update([ww for ww in words if w in ww])
#            for word in [ww for ww in words if w in ww]:
#                y=input('Do you want to blacklist "%s" (y/N): ' % word)
#                if y.lower().strip() == 'y':
#                    blacklisted.add(word)
    except EOFError:
        with open(args.output_file, 'w') as file:
            print("Saving...")
            for word in blacklisted:
                file.write("%s\n" % word)
