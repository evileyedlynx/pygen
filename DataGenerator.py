import json

from Node import Node
import generator_log as log


class DataGenerator:
    _nodes = []
    _path_to_save_files = None
    _files_count = None
    _file_name = None
    _data_lines = None
    _show_generated_data = None
    _show_write_in_file = None
    _generate_node_log = None

    def __init__(self, scheme: str,
                 path_to_save_files: str,
                 files_count: int,
                 file_name: str,
                 data_lines: int,
                 show_generated_data=False,
                 show_write_in_file=False,
                 generate_node_log=False):
        """
        Datagenereator object init.

        :param scheme: object generation scheme.
        :param path_to_save_files: path for saving files.
        :param files_count: amount of files to generate.
        :param file_name: base file names.
        :param data_lines: amount of strings with generated data in created files.
        :param show_generated_data: flag to show log of DataGenerator. False by default.
        :param show_write_in_file: flag to show data written in file. False by default.
        :param generate_node_log: flag to show log of "Node" class work. False by default.
        """
        self._path_to_save_files = path_to_save_files
        self._files_count = files_count
        self._file_name = file_name
        self._data_lines = data_lines
        self._show_generated_data = show_generated_data
        self._show_write_in_file = show_write_in_file
        self._generate_node_log = generate_node_log
        self.parse_json_to_node(scheme)

    def parse_json_to_node(self, json_scheme):
        """
        Parse json schema to Node objects.

        :param json_scheme: json data scheme file. ./schemas/main.json by default.
        """
        try:
            for data in json_scheme:
                schema = json_scheme.get(data)
                if schema:
                    node = Node(data, schema, self._generate_node_log)
                    self.add_value_in_nodes(node)
                else:
                    log.error('Scheme is None')
            log.info(f'{"Successful parse json to Nodes"}')
        except Exception as e:
            log.error(f'Error when parse schema: {str(e)}')

    @property
    def nodes(self):
        """Getter of self._nodes var."""
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        """Setter of self._nodes var."""
        self._nodes = value

    def add_value_in_nodes(self, value: Node):
        """Adding var to self._nodes."""
        self._nodes.append(value)

    def generate_data(self):
        """
        Data generation based on created Node object
        Writing result based on set parameters
        """
        lines_count = 0
        file_count = 1
        all_lines_count = 0
        file_path = f'{self._path_to_save_files}/{self._file_name}.jsonl'
#        try:
#            file_path = f'{self._path_to_save_files}/{self._file_name}.jsonl'
#            f = open(file_path, 'w+', encoding='utf-8')
#            log.info(f'{file_path} created')
#        except Exception as e:
#            log.error(f'Failed create file {file_path}: {e}')
        log.info(f'Starting generate data. count: {self._files_count}')
        for amount in range(self._files_count):
            try:
                if lines_count >= self._data_lines:
#                    f.close()
#                    new_file_path = f'{self._path_to_save_files}/{self._file_name}_{str(file_count)}.jsonl'
                    file_path = f'{self._path_to_save_files}/{self._file_name}_{str(file_count)}.jsonl'
#                    f = open(new_file_path, 'w+', encoding='utf-8')
                    file_count += 1
                    lines_count = 0
                    if self._show_write_in_file:
#                        log.info(f'Created new file {new_file_path}')
                        log.info(f'Created new file {file_path}')
            except Exception as e:
                log.error(f'Failed create new file: {e}')

            for line in range(self._data_lines):
                try:
                    node_result = {}
                    for node in self.nodes:

                        node_result[node.node_name] = node.generate_data()
                    json_data = json.dumps(node_result)
                    if self._show_generated_data:
                        log.info(f'data made: {node_result}')
                except Exception as e:
                    log.error(f'Error generating data: {e}')

                try:
                    f = open(file_path, 'a', encoding='utf-8')
                    f.write(f'{json_data}\n')
                    f.close()
                    if self._show_write_in_file:
                        log.info(f'{"data written in file"}')
                except Exception as e:
                    log.error(f'Error when try write data in file: {e}')
                lines_count += 1
                all_lines_count += 1
                log.info(f'made {str(all_lines_count)}/{str(self._files_count)} datas. made {file_count} files')
                # print(node_result)

        print(f'Data generation ended')
