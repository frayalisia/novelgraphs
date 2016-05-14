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
<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>SentenceID</th>\n      <th>TokenID</th>\n      <th>Token</th>\n      <th>Lemma</th>\n      <th>Pos</th>\n      <th>NER</th>\n      <th>DepParse</th>\n      <th>DepRel</th>\n      <th>NerNpID</th>\n      <th>Sentiment</th>\n      <th>QuotationID</th>\n      <th>DialogID</th>\n      <th>CharacterID</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>0</td>\n      <td>0</td>\n      <td>A</td>\n      <td>a</td>\n      <td>DT</td>\n      <td>O</td>\n      <td>1</td>\n      <td>det</td>\n      <td>None</td>\n      <td>NaN</td>\n      <td>None</td>\n      <td>None</td>\n      <td>None</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>0</td>\n      <td>1</td>\n      <td>STUDY</td>\n      <td>study</td>\n      <td>NN</td>\n      <td>O</td>\n      <td>-1</td>\n      <td>ROOT</td>\n      <td>None</td>\n      <td>NaN</td>\n      <td>None</td>\n      <td>None</td>\n      <td>None</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>0</td>\n      <td>2</td>\n      <td>IN</td>\n      <td>in</td>\n      <td>IN</td>\n      <td>O</td>\n      <td>4</td>\n      <td>case</td>\n      <td>None</td>\n      <td>NaN</td>\n      <td>None</td>\n      <td>None</td>\n      <td>None</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>0</td>\n      <td>3</td>\n      <td>SCARLET</td>\n      <td>scarlet</td>\n      <td>NNP</td>\n      <td>O</td>\n      <td>4</td>\n      <td>compound</td>\n      <td>None</td>\n      <td>NaN</td>\n      <td>None</td>\n      <td>None</td>\n      <td>None</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>0</td>\n      <td>4</td>\n      <td>Table</td>\n      <td>table</td>\n      <td>NNP</td>\n      <td>O</td>\n      <td>1</td>\n      <td>nmod:in</td>\n      <td>None</td>\n      <td>NaN</td>\n      <td>None</td>\n      <td>None</td>\n      <td>None</td>\n    </tr>\n  </tbody>\n</table>

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
