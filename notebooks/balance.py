import pandas as pd
import networkx as nx
import numpy
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.abspath('../novelgraphs/'))

import novelgraphs as ng

def graph_weights(graph):
    return [edge[2]['weight'] for edge in graph.edges(data=True)]

def rolling_window_slices(window_size, step, length):
    '''Скользящее окно'''
    if length <= 18000:
        window_size = 3000
        step = 1000
    
    num_slices = max((length - window_size) // step, 0)
    return ([slice(i * step, i * step + window_size) for i in range(num_slices)] +
             [slice(num_slices * step, length)])

def get_chapters(window_size, step, length, text):
    '''Делим скользящим окном текст на главы'''
    chapters = []
    for slice_t in rolling_window_slices(window_size, step, length):
        tags = text.tags.loc[slice_t]
        chapter = ng.Text('')
        chapter.characters = text.characters
        chapter.first_person = text.first_person
        chapter.tags = tags
        chapters.append(chapter)
    return chapters

def get_negative_sentiment_balance(chapters, novelgraph):
    '''Считаем долю отрицательных ребер среди всех в графе'''
    text_balance = []
    for i in range(len(chapters)):
        graph = novelgraph(chapters[i])
        weights = graph_weights(graph)
        if weights:
            balance = len([p for p in weights if p < 0]) / len(weights)
            text_balance.append(balance)
    return text_balance

def get_cycles_from_graph(graph):
    '''Выделяем циклы из графа'''
    cycles = []
    for cycle in nx.cycle_basis(graph):
        cycles.append(list(zip(cycle, cycle[1:])) + [(cycle[-1], cycle[0])])
    return cycles

def is_positive(cycle, graph):
    '''Определяем знак графа - если число негативных ребер четное, тогда граф позитивный, 
    если нечетное - тогда негативный'''
    negatives = 0
    for edge in cycle:
        if graph.edge[edge[0]][edge[1]]['weight'] < 0:
            negatives += 1
    return not negatives % 2

def get_graph_balance(chapters, novelgraph):
    '''Считаем сбалансированность графа: 
    1. выделить простые циклы из графа
    2. определить знак цикла
    3. находим меру сбалансированности - долю положительных циклов среди всех
    '''
    balance_cycle = []
    for i in range(len(chapters)):
        graph = novelgraph(chapters[i])
        graph_cycles = get_cycles_from_graph(graph)
#         print(len(graph_cycles))
        balance = numpy.mean(
            [is_positive(cycle, graph) for cycle in graph_cycles])
        balance_cycle.append(balance)
#     print(balance_cycle) 
    return balance_cycle

def negative_sentiment(window_size, step, length, novelgraph, text):
    chapters = get_chapters(window_size, step, length, text)
    negative_graph = get_negative_sentiment_balance(chapters, novelgraph)
    return plt.plot(negative_graph, label='Negative_sentiment')

def graph_balance(window_size, step, length, novelgraph, text):
    chapters = get_chapters(window_size, step, length, text)
    balance = get_graph_balance(chapters, novelgraph)
    return plt.plot(balance, label='Balance')
