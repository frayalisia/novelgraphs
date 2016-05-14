# NovelGraphs
Python3 tool for automatic text annotation and extraction networks of characters

# Features
* automatic text annotation (using Stanford CoreNLP)
* new algorithm for characters' detection
* different exctractors of relationships between characters
* plotting balance of text
* sentiment analysis (using [AFINN-111](https://github.com/wooorm/afinn-111))

# Dependencies
- NetworkX
- pandas
- numpy
- [Stanford CoreNLP pack](http://stanfordnlp.github.io/CoreNLP/index.html)
- nltk

# Installation
```git clone https://github.com/frayalisia/novelgraphs.git```

# Basic usage
###Import module
```python
import novelgraphs as ng
```
### Import annonators
```python
core = ng.annotators.CoreNLP()
np = ng.annotators.NerNpID()
senti = ng.annotators.Sentiment()
```

### Wrap file
```python
text = ng.Text('some text is here', corenlp_path='path to CoreNLP library')
```

### Make annotation pipeline
```python
pipeline = ng.annotators.Pipeline([core, np, senti])
pipeline.annotate(text)
```

### Import extractors and aggregators
```python
dialog = ng.interaction.extractors.Dialog()
sentences = ng.interaction.extractors.Sentences()

count = ng.interaction.aggregators.Count()
sentiment = ng.interaction.aggregators.Sentiment()
```

### Make graph
```python
novelgraph = ng.NovelGraph(extractor, aggregator)
graph = novelgraph(text)
```

### Visualize graph
```python
nx.draw_networkx(graph, with_labels=True)
```

### Plot balance
```python
from balance import graph_balance

graph_balance(window_size, step, text_length, novelgraph, text)
```

# TODO
- [ ] Coreference resolution
- [ ] Clustering (disambiguation) characters names
      * _h. golaytly_
      * _holly golaytly_
      * _holly_
      * _miss golaytly_
- [ ] Identification narrator with character (by "I am ...", "My name is ...", "They called me ...")
- [ ] Add rules to Universal Quote annotator (distance between speech and context, check words like 'speak\say' in context)
- [ ] Second "wave" of NER-annotation (+ Mrs., Mr.)
- [ ] Add non-NER characters
