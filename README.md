# NovelGraphs
Python3 tool for automatic text annotation and extraction networks of characters

# Features
* automatic text annotation (using Stanford CoreNLP)
* new algorithm for characters' detection
* different exctractors of relationships between characters
* plotting balance of text
* sentiment analysis (using [AFINN-111](https://github.com/wooorm/afinn-111))

# Dependencies
- networkx >= 1.10
- pandas >= 0.18.0
- numpy >= 1.10.4
- nltk >= 3.1
- [Stanford CoreNLP pack](http://stanfordnlp.github.io/CoreNLP/index.html)

# Installation
```git clone https://github.com/frayalisia/novelgraphs.git```

# Basic usage
###Import module
```python
import novelgraphs as ng
```

### Wrap file
```python
text = ng.Text('some text is here', corenlp_path='path to CoreNLP library')
```

### Import annonators
```python
core = ng.annotators.CoreNLP()
np = ng.annotators.NerNpID()
senti = ng.annotators.Sentiment()
```
Annotators | Annotation
--- | --- 
[CoreNLP] (http://stanfordnlp.github.io/CoreNLP) | pos, lemma, ner, parse (syntax dependencies) 
QuotationID | quote id (find quotes in text)
NerNpID | ner id (find complex ner-items)
Sentiment | sentiment of words (using [AFINN-111] (https://github.com/fnielsen/afinn))
DialogID | dialog id (collect quotes to the dialog)
DialogOutQuotesID | dialog without quotes (only remarks)
FirstPerson | find narrator in text
Character | character id (find characters in text)


### Make annotation pipeline
```python
pipeline = ng.annotators.Pipeline([core, np, senti])
pipeline.annotate(text)
```
To make pipeline easier, look at dependencies between different annotators.

| Annotator | Dependencies | Dependencies | Dependencies |
| --- | --- | --- | --- |
| CoreNLP | 
| QuotationID | 
| NERNpID | CoreNLP | 
| Sentiment | CoreNLP | 
| DialogID | QuotationID |
| DialogOutQuotesID | DialogID | QuotationID
| FirstPerson | CoreNLP | QuotationID |
| Character | CoreNLP | NERNpID | FirstPerson | 


Annotated table will look like this. 
<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">     <th></th>      <th>SentenceID</th>      <th>TokenID</th>      <th>Token</th>      <th>Lemma</th>      <th>Pos</th>      <th>NER</th>      <th>DepParse</th>      <th>DepRel</th>      <th>NerNpID</th>      <th>Sentiment</th>      <th>QuotationID</th>      <th>DialogID</th>      <th>CharacterID</th>    </tr>  </thead>  <tbody>   <tr>      <th>0</th>      <td>0</td>      <td>0</td>      <td>A</td>     <td>a</td>     <td>DT</td>     <td>O</td>      <td>1</td>      <td>det</td>      <td>None</td>      <td>NaN</td>      <td>None</td>      <td>None</td>      <td>None</td>    </tr>    <tr>      <th>1</th>      <td>0</td>      <td>1</td>      <td>STUDY</td>      <td>study</td>      <td>NN</td>      <td>O</td>      <td>-1</td>      <td>ROOT</td>      <td>None</td>      <td>NaN</td>      <td>None</td>      <td>None</td>      <td>None</td>    </tr>    <tr>      <th>2</th>      <td>0</td>      <td>2</td>      <td>IN</td>      <td>in</td>      <td>IN</td>      <td>O</td>      <td>4</td>      <td>case</td>      <td>None</td>      <td>NaN</td>      <td>None</td>      <td>None</td>      <td>None</td>    </tr>    <tr>      <th>3</th>      <td>0</td>      <td>3</td>      <td>SCARLET</td>      <td>scarlet</td>      <td>NNP</td>      <td>O</td>      <td>4</td>      <td>compound</td>      <td>None</td>      <td>NaN</td>      <td>None</td>      <td>None</td>      <td>None</td>    </tr>    <tr>      <th>4</th>      <td>0</td>      <td>4</td>      <td>Table</td>      <td>table</td>      <td>NNP</td>      <td>O</td>      <td>1</td>      <td>nmod:in</td>      <td>None</td>      <td>NaN</td>      <td>None</td>      <td>None</td>      <td>None</td>    </tr>  </tbody></table>

### Import extractors and aggregators
##### How to import
```python
dialog = ng.interaction.extractors.Dialog()

count = ng.interaction.aggregators.Count()
```
##### About extractors and aggregators
Extractors | How-to
--- | ---
TokenDistance | distance between characters is n-tokens (n=15)
Sentence | characters are in 1 sentence 
SentenceDistance | distance between characters is not more than n-sentences (n=2) 
Dialog | characters are in 1 dialog
DialogWithoutQuote | characters in 1 dialog (except quotes)
TokenSequence | character--verb--character
TokenDependencies | character ... --verb-- ...character (+ syntactic dependencies between verb and characters)

Aggregators | How-to
--- | ---
Count | frequency of interactions between characters
Sentiment | average sentiment for the context, where characters interact

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
