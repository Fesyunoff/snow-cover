#!/usr/bin/env python
# -*- encoding: koi8-r -*-

import os
import sys
import json
import entities as ent


def main():

    directory = './samples/'
    output_file_name = 'output.json'
    verbose = False

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    if len(sys.argv) > 2:
        output_file_name = sys.argv[2]
    if len(sys.argv) > 3:
        if sys.argv[3] == 'v':
            verbose = True

    file_list = os.listdir(path=directory)
    with open(output_file_name, 'w') as output_file:
        if verbose:
            print('output_file "'+output_file_name+'" created')
        print('INFO: from the directory "'+directory+'" received files:')
        for file_name in file_list:
            print(file_name)
            with open(directory+file_name, 'rb') as input_file:
                content = input_file.read().decode("koi8-r")
                rows = list(map(str, content.split('=')))
                for row in rows:
                    row = row.strip('HHSS \x0fHHSS \n \r')
                    if verbose:
                        print('\n', row, '\n')
                    snow_cover = ent.Snow_cover(row)
                    out = snow_cover.get_snow_cover()
                    for line in out:
                        line = json.dumps(line)
                        if verbose:
                            print(line)
                        output_file.write(line + '\n')

                            #  print(json.dumps(line))
                        #  output_file.write(json.dumps(line) + '\n')

    print('INFO: all lines are written to file: "'+output_file_name+'"')
    output_file.close()

if __name__ == "__main__":
    main()  


