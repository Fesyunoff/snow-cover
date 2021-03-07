#!/usr/bin/env python
# -*- encoding: koi8-r -*-

import os
import sys
import logging
import json
import entities as ent


def main():
    directory = './samples'
    output_file_path = './output.json'
    loglevel = logging.INFO
    encoding = 'koi8-r'

    if len(sys.argv) > 1:
        directory = sys.argv[1]
        if len(sys.argv) > 2:
            output_file_name = sys.argv[2]
            if len(sys.argv) > 3:
                if sys.argv[3] == 'debug':
                    loglevel = logging.DEBUG

    logging.basicConfig(format='%(asctime)s |%(levelname)s| %(message)s',
                        datefmt='%H:%M:%S',
                        level=loglevel)
    file_list = os.listdir(path=directory)

    with open(output_file_path, 'w') as output_file:
        logging.debug('output file "'+output_file_path+'" was open')
        logging.info('INFO: from the directory "'+directory+'" received files:')
        for file_name in file_list:
            path = os.path.join(directory, file_name)
            logging.info(file_name)
            with open(path, 'rb') as input_file:
                content = input_file.read().decode(encoding)
                rows = content.split('=')
                for row in rows:
                    row = row.strip('HHSS \x0fHHSS \n \r')
                    if len(row) > 0:
                        logging.debug('RAW: '+row)
                        snow_cover = ent.SnowCover(row)
                        out = snow_cover.get_snow_cover()
                        for line in out:
                            line = json.dumps(line)
                            logging.debug('JSON: '+line)
                            output_file.write(line + '\n')

    logging.info('all lines are written to file: "'+output_file_path+'"')

if __name__ == "__main__":
    main()  


