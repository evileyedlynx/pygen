import re
import time
import uuid
import random
import generator_log as log


class Node:
    _node_name: str = None
    _node_type = None
    _data_generate_rule = None
    _generate_node_log = None

    def __init__(self, node_name: str, scheme: str, generate_node_log=False):
        """
        Object init.
        :param node_name: Name of value.
        :param scheme: Data generation scheme.
        :param generate_node_log: Show data generation log. False by default.
        """
        self._generate_node_log = generate_node_log
        self.node_name = node_name
        node_data = scheme.split(':')
        try:
            self.node_type = node_data[0]
        except IndexError as e:
            log.error(f'Array node_data is empty - {e}')

        try:
            if node_data[0] == 'timestamp':
                self.data_generate_rule = node_data[1]
                log.warning('timestamp type does not support any values and ignored')
            else:
                self.data_generate_rule = node_data[1]
        except IndexError as e:
            log.error(f'Index error when trying to set data_generate_rule: {e}')
        log.info(f'{node_name} initialize successful')

    @property
    def node_name(self) -> str:
        """Getter of var self._node_name."""
        return self._node_name

    @node_name.setter
    def node_name(self, value: str):
        """Setter of var self._node_name."""
        self._node_name = value

    @property
    def node_type(self) -> str:
        """Getter of var self._node_type."""
        return self._node_type

    @node_type.setter
    def node_type(self, value):
        """Setter of var self._node_type."""
        accepted_values = [
            'timestamp',
            'str',
            'int'
        ]
        if value in accepted_values:
            self._node_type = value
            log.info(f'for {self.node_name} set {value} type')
        else:
            log.error(f'Error when try set node_type. Unknown type: {value}')

    @property
    def data_generate_rule(self):
        """Getter of var self._data_generate_rule."""
        return self._data_generate_rule

    @data_generate_rule.setter
    def data_generate_rule(self, value):
        """Setter of var self._data_generate_rule."""
        self._data_generate_rule = value

    def generate_data(self):
        """
        Data generation based on scheme, transferred here at the object initialization time.

        :return: Returns generated data.
        """
        result = None
        try:
            if self.node_type == 'timestamp':
                if self._generate_node_log:
                    log.generate_data(self.node_name, result)
                return time.time()

            if self.data_generate_rule == '':
                match self.node_type:
                    case 'int':
                        if self._generate_node_log:
                            log.generate_data(self.node_name, result)
                        return None
                    case 'str':
                        if self._generate_node_log:
                            log.generate_data(self.node_name, result)
                        return ''
                    case _:
                        log.unknown_type(self.data_generate_rule)

            if self.data_generate_rule == 'rand':
                match self.node_type:
                    case 'str':
#                        result = str(uuid.uuid4())
                        if self._generate_node_log:
                            log.generate_data(self.node_name, result)
                        return str(uuid.uuid4())
                    case 'int':
#                        result = random.randint(0, 10000)
                        if self._generate_node_log:
                            log.generate_data(self.node_name, result)
                        return random.randint(0, 10000)
                    case _:
                        log.unknown_type(self.node_type)
        except TypeError as e:
            log.error(f'Error when try get time, None or \'\' or "rand" data: {e}')

        try:
            random_regex = re.findall(r'rand\([-+]?\d+, [-+]?\d+\)', self.data_generate_rule)
            if len(random_regex) == 1 and random_regex[0] == self.data_generate_rule and self.node_type == 'int':
                nums = [int(s) for s in re.findall(r'\d+', random_regex[0])]
                if len(nums) == 2:
                    first_number = nums[0]
                    second_number = nums[1]
                else:
                    if self._generate_node_log:
                        log.info(f'More numbers in {random_regex}.')

                if first_number < second_number:
                    result = random.randint(first_number, second_number)
                    if self._generate_node_log:
                        log.generate_data(self.node_name, result)
                    return result
                else:
                    if self._generate_node_log:
                        log.info(f'First number is greater than second. First: {first_number}, Second: {second_number}.')
        except Exception as e:
            log.error(f'Error when try generate "rand(x, y)" data: {e}')

        try:
            if isinstance(eval(self.data_generate_rule), list):
                result = random.choice(eval(self.data_generate_rule))
                match self.node_type:
                    case 'str':
                        if self._generate_node_log:
                            log.generate_data(self.node_name, result)
                        return str(result)
                    case 'int':
                        if self._generate_node_log:
                            log.generate_data(self.node_name, result)
                        return int(result)
                    case _:
                        log.unknown_type(self.data_generate_rule)
        except ValueError as e:
            if self._generate_node_log:
                log.info(f'Specified data type is not list: {e}')

        try:
            match self.node_type:
                case 'int':
                    if self._generate_node_log:
                        log.generate_data(self.node_name, result)
                    return int(self.data_generate_rule)
                case 'str':
                    if self._generate_node_log:
                        log.generate_data(self.node_name, result)
                    return str(self.data_generate_rule)
        except ValueError as e:
            log.error(f'\'{self.data_generate_rule}\' cannot be converted to type: {e}')



        log.error('No data type found')
