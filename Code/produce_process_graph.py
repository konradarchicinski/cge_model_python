import os
import argparse
from pathlib import Path
from graphviz import Digraph

work_dir = str(Path(os.path.realpath(__file__)).parents[1])

def produce_process_graph(graphviz_installation_path):
    '''
    Usually Social Accounting Matrix datasets are build in hard to operate way,
    this funtion...

    To prepare data for analysis user has to...
    '''
    os.environ["PATH"] += os.pathsep + graphviz_installation_path + '\\bin\\'

    e = Digraph('PROCESS', directory=work_dir, filename='Process Graph.gv', engine='neato', format='pdf')

    e.attr('node', shape='box')
    e.node('produce_process_graph.py')
    e.node('sam_partition.py')
    e.node('model.py')

    e.attr('node', shape='oval')
    e.node('Dashboard')

    e.attr('node', shape='note')
    e.node('Graph')

    e.attr('node', shape='parallelogram', style='filled')
    e.node('SAM data')
    e.node('SAM data csv')
    e.node('Results DB')

    e.edge('Dashboard', 'SAM data', label='Data file used', len='4.00')
    e.edge('SAM data', 'sam_partition.py', len='2.00')
    e.edge('sam_partition.py','SAM data csv', label='sam_data_preparation', len='4.00')
    e.edge('SAM data csv', 'model.py', len='2.00')
    e.edge('Dashboard', 'model.py',label='Anticipated shocks' , len='4.00')
    e.edge('model.py', 'Results DB', len='2.00')
    e.edge('Results DB', 'Dashboard', len='2.00')

    e.edge('produce_process_graph.py', 'Graph', label="produce_process_graph", len='3.00')

    e.attr(label=r'\n\nProcess Graph')
    e.attr(fontsize='20')

    e.view()
    

def main():
    
    parser = argparse.ArgumentParser(
        description='''
        Program used to create the process graph helping better workflow understanding.
        '''
    )
    parser.add_argument(
        'graphviz_installation_path', 
        type=str,
        nargs='?', 
        default="C:\\Program Files (x86)\\Graphviz2.38", 
        help="""
        Directory path to folder in which is installed Graphviz software.
        """
    )
    args = parser.parse_args()

    produce_process_graph(args.graphviz_installation_path)


if __name__ == "__main__":

    main()