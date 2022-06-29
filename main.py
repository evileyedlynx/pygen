import argparse
import configparser
import json
import os
import random
import string
import uuid

from DataGenerator import DataGenerator
import generator_log as log

config = configparser.ConfigParser()
config.read('default.ini')


def main():
    prefixes = ['count', 'random', 'uuid']
    print("*********  This is Pygen utility **********")
    path_to_save_files = config['DEFAULT']['path_to_save_files']
    files_count = config['DEFAULT']['files_count']
    file_name = config['DEFAULT']['file_name']
    file_prefix = config['DEFAULT']['file_prefix']
    data_schema = config['DEFAULT']['data_schema']
    data_lines = config['DEFAULT']['data_lines']
    clear_path = config.getboolean('DEFAULT', 'clear_path')
    show_generated_data = config.getboolean('DEFAULT', 'show_generated_data')
    show_write_in_file = config.getboolean('DEFAULT', 'show_write_in_file')
    show_generate_node_log = config.getboolean('DEFAULT', 'show_generate_node_log')
    log_in_file = config.getboolean('DEFAULT', 'log_in_file')

    parser = argparse.ArgumentParser(description='CU for generating data by scheme')
    parser.add_argument('--path_to_save_files', help="Where all the files will be saved", type=str, default=path_to_save_files)
    parser.add_argument('--files_count', help="How many json files to generate", type=int, default=files_count)
    parser.add_argument('--file_name', help="Base file_name. If no prefix, final file name will be file_name.json. With prefix full file name will be file_name_file_prefix.json", type=str, default=file_name)
    parser.add_argument('--file_prefix', help="What prefix for file name to use if more than 1 file needs to be generated", choices=prefixes, type=str)
    parser.add_argument('--data_schema', help="It’s a string with json schema", type=str, default=data_schema)
    parser.add_argument('--data_lines', help="Count of lines for each file", type=int, default=data_lines)
    parser.add_argument('--clear_path', help="If this flag is on, before the script starts creating new data files, all files in path_to_save_files that match file_name will be deleted.", default=clear_path, action='store_true')
    parser.add_argument('--show_generated_data', help="If this flag is on, show generated data in console.", default=show_generated_data, action='store_true')
    parser.add_argument('--show_write_in_file', help="If this flag is on, show log when data write in file.", default=show_write_in_file, action='store_true')
    parser.add_argument('--show_generate_node_log', help="If this flag is on, node generation log.", default=show_generate_node_log, action='store_true')
    parser.add_argument('--log_in_file', help="If this flag is on, enable logging in file.", default=log_in_file, action='store_true')
    args = parser.parse_args()

    if args.log_in_file:
        log.logging_in_file(args.file_name)

    if os.path.exists(args.path_to_save_files):
        if os.path.isdir(args.path_to_save_files):
            if args.files_count < 0:
                log.error('Files count < 0')
            else:
                filename = args.file_name
                match args.file_prefix:
                    case 'count':
                        filename += str('_' + str(args.files_count))
                        log.info(f'Selected count prefix. filename: {filename}')
                    case 'random':
                        filename += '_'.join(random.choice(string.ascii_lowercase) for i in range(10))
                        log.info(f'Selected random prefix. filename: {filename}')
                    case 'uuid':
                        filename += str('_' + uuid.uuid4())
                        log.info(f'Selected uuid prefix. filename: {filename}')
                    case 'none':
                        log.info('Did not use prefix')

                scheme = read_json(args.data_schema)
                if scheme is None:
                    try:
                        with open(args.data_schema) as f:
                            scheme = json.load(f)
                            log.info(f'Scheme loaded from file: {scheme}')
                    except Exception as e:
                        log.error(f'Error when try read data schema from file: {e}')
                else:
                    log.info(f'Scheme loaded from args: {scheme}')

                if args.clear_path:
                    try:
                        for file in os.listdir(args.path_to_save_files):
                            if args.file_name in file:
                                file_path = f'{args.path_to_save_files}/{file}'
                                os.remove(file_path)
                                log.info(f'{file_path} deleted')
                    except Exception as e:
                        log.error(f'Error when try remove file {file_path}: {e}')

                generator = DataGenerator(scheme, args.path_to_save_files, args.files_count, filename, args.data_lines, args.show_generated_data, args.show_write_in_file, args.show_generate_node_log)
                generator.generate_data()
        else:
            log.error('Path os not a directory')
    else:
        log.error('path does not exist')


def read_json(json_schema):
    try:
        scheme = json.loads(json_schema)
        return scheme
    except ValueError:
        return None
    except Exception as e:
        log.error(f'Error when try read scheme from args: {e}')
    # scheme_json = '{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"str:[\'client\', \'partner\', \'government\']\",\"age\": \"int:rand(1, 90)\"}'
    # generator = DataGenerator(scheme_json)
    # generator.generate_data(5)


if __name__ == '__main__':
    main()
