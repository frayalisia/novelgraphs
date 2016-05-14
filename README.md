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
Annotated table will look like this. 
<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">     <th></th>      <th>SentenceID</th>      <th>TokenID</th>      <th>Token</th>      <th>Lemma</th>      <th>Pos</th>      <th>NER</th>      <th>DepParse</th>      <th>DepRel</th>      <th>NerNpID</th>      <th>Sentiment</th>      <th>QuotationID</th>      <th>DialogID</th>      <th>CharacterID</th>    </tr>  </thead>  <tbody>   <tr>      <th>0</th>      <td>0</td>      <td>0</td>      <td>A</td>     <td>a</td>     <td>DT</td>     <td>O</td>      <td>1</td>      <td>det</td>      <td>None</td>      <td>NaN</td>      <td>None</td>      <td>None</td>      <td>None</td>    </tr>    <tr>      <th>1</th>      <td>0</td>      <td>1</td>      <td>STUDY</td>      <td>study</td>      <td>NN</td>      <td>O</td>      <td>-1</td>      <td>ROOT</td>      <td>None</td>      <td>NaN</td>      <td>None</td>      <td>None</td>      <td>None</td>    </tr>    <tr>      <th>2</th>      <td>0</td>      <td>2</td>      <td>IN</td>      <td>in</td>      <td>IN</td>      <td>O</td>      <td>4</td>      <td>case</td>      <td>None</td>      <td>NaN</td>      <td>None</td>      <td>None</td>      <td>None</td>    </tr>    <tr>      <th>3</th>      <td>0</td>      <td>3</td>      <td>SCARLET</td>      <td>scarlet</td>      <td>NNP</td>      <td>O</td>      <td>4</td>      <td>compound</td>      <td>None</td>      <td>NaN</td>      <td>None</td>      <td>None</td>      <td>None</td>    </tr>    <tr>      <th>4</th>      <td>0</td>      <td>4</td>      <td>Table</td>      <td>table</td>      <td>NNP</td>      <td>O</td>      <td>1</td>      <td>nmod:in</td>      <td>None</td>      <td>NaN</td>      <td>None</td>      <td>None</td>      <td>None</td>    </tr>  </tbody></table>

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
Here is final graph.
![Final graph of the novel "Study in Scarlet" by Conan Doyle](https://cloud.githubusercontent.com/assets/17455391/15270270/88a9fbe6-1a2a-11e6-9db4-5b1d719f46e8.png)

### Plot balance
```python
from balance import graph_balance

graph_balance(window_size, step, text_length, novelgraph, text)
```
Text balance produces the balance plot.
![Text balance of the novel "Study in Scarlet" by Conan Doyle](https://cloud.githubusercontent.com/assets/17455391/15270275/b2157dd4-1a2a-11e6-8e45-bfe6238ecdec.png)

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
