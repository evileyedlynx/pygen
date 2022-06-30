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
        self._path_to_save_files = path_to_save_files
        self._files_count = files_count
        self._file_name = file_name
        self._data_lines = data_lines
        self._show_generated_data = show_generated_data
        self._show_write_in_file = show_write_in_file
        self._generate_node_log = generate_node_log
        self.parse_json_to_node(scheme)

    def parse_json_to_node(self, json_scheme):
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
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

    def add_value_in_nodes(self, value: Node):
        self._nodes.append(value)

    def generate_data(self):
        lines_count = 0
        file_count = 1
        all_lines_count = 0
        try:
            file_path = f'{self._path_to_save_files}/{self._file_name}.jsonl'
            f = open(file_path, 'w+', encoding='utf-8')
            log.info(f'{file_path} created')
        except Exception as e:
            log.error(f'Failed create file {file_path}: {e}')
        log.info(f'Starting generate data. count: {self._files_count}')
        for amount in range(self._files_count):
            try:
                if lines_count >= self._data_lines:
                    f.close()
                    new_file_path = f'{self._path_to_save_files}/{self._file_name}_{str(file_count)}.jsonl'
                    f = open(new_file_path, 'w+', encoding='utf-8')
                    file_count += 1
                    lines_count = 0
                    if self._show_write_in_file:
                        log.info(f'Created new file {new_file_path}')
            except Exception as e:
                log.error(f'Failed create new file: {e}')

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
                f.write(f'{json_data}\n')
                if self._show_write_in_file:
                    log.info(f'{"data written in file"}')
            except Exception as e:
                log.error(f'Error when try write data in file: {e}')
            lines_count += 1
            all_lines_count += 1
            log.info(f'made {str(all_lines_count)}/{str(self._files_count)} datas. made {file_count} files')
            # print(node_result)

        print(f'{"Data generation ended"}')
