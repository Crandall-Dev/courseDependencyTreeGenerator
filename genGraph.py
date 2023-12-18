#!/usr/bin/env python3

import csv
import logging
from pprint import pprint

import networkx as nx
import matplotlib.pyplot as plt

class Class:
    def __init__(self, csv_dependencies: dict):
        self._csv_dependencies = csv_dependencies
        self._number = csv_dependencies['Number']
        self._name = csv_dependencies['Name']
        self._prerequisites = csv_dependencies['Prerequisites']
        self._required = csv_dependencies['BS CS Required']

    def __str__(self):
        return f'CPSC {self._number} - {self._name} || Prereqs: {self._prerequisites}'
    
    def get_name(self) -> str:
        return self._name
    
    def get_number(self) -> str:
        return self._number
    
    def is_required(self) -> bool:
        return self._required == 'X'
    
    def get_dependencies(self) -> list:
        dependencies = []

        raw_dependencies = self._prerequisites.split(' ')
        for dependency in raw_dependencies:
            if dependency in ['None', '', 'and', 'or']:
                continue
            new_dependency = (self._number, dependency)
            dependencies.append(new_dependency)

        return dependencies




# ****************************************************************** #
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    csv_file_path = 'dependencies.csv'

    classes = []

    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
    
        columns = csv_reader.fieldnames
    
        for row in csv_reader:
            logging.debug(row)
            curr_class = Class(row)
            classes.append(curr_class)

    dependency_tree = nx.DiGraph()

    node_order = []
    for curr_class in classes:
        node_order.append(curr_class.get_number())
    dependency_tree.add_nodes_from(node_order)

    dependencies = []

    for curr_class in classes:
        dependencies.extend(curr_class.get_dependencies())

    dependency_tree.add_edges_from(dependencies)

    node_size = 500

    node_colors = []
    for curr_class in classes:
        if curr_class.is_required():
            node_colors.append('green')
        else:
            node_colors.append('yellow')

    # Visualize the dependency tree
    # pos = nx.spring_layout(dependency_tree)  # You can use different layout algorithms
    pos = nx.nx_agraph.graphviz_layout(dependency_tree, prog='dot', args='-Grankdir=RL')
    nx.draw(dependency_tree, pos, with_labels=True, arrows=True, node_size=node_size, node_color=node_colors)
    plt.title('Dependency Tree')
    plt.show()
