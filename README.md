# path2vec
An extension of the idea in [Dependency-Based Word Embeddings](https://aclanthology.org/P14-2050.pdf) [(code)](https://github.com/BIU-NLP/word2vecf) that adds dependency paths as keys in the embedding space. The additional embeddings can be inspected and used as the basis for query expansion in the case of natural language information retrieval.

This repo includes:
- A spaCy-based data pipeline for extracting dependency encoded word-context pairs
- Additional context pairs extracted for dependency path triples
- An implementation of the original paper's arbitary context word2vec in pytorch

## Data Pipeline
To run the pipeline yourself you will need to add an input text corpus to `/data/corpora/`.
I used a recent-ish xml [Wikipedia dump](https://dumps.wikimedia.org/), extracted and cleaned using [WikiExtractor](https://github.com/attardi/wikiextractor).
The pipeline is organized into a series of notebook stages that save their output artifacts to relevant folders in `/data/`. The initial `parse` stage is by far the longest and may need to be split up and managed over several days, hardware depending.

### 0_parse
Use the selected spaCy pipeline to get tokenization, pos, and dependency parses. Outputs are saved in spaCy's `DocBin` format, with each file containing 1000 parsed texts with a shared vocabulary to cut down on disk space and make it easier to handle batches of parse files. Progress is saved in order to resume processing a given input corpus, allowing for incrimental batches & experimentation.

### 1_triples
Runs each resulting parse through an additional set of rule-based dependency matchers to extract a particular set of IE triples. As an example, in the sentence 'Alice is the queen of Antarctica' the triple (alice)-[be_queen_of]->(antarctica) would be extracted. Examples of the kinds of multi-hop triples which are being detected can be found in `pathvecs/matchers/triples`, which were hand-derived from a frequency analysis and comparison of paths connecting nominals in a sample corpus. These are in addition to single-hop dependency triples, which are extracted as per the original paper - prepositional phrases are shortened to span the preposition itself as if it were a dependency edge e.g., 'a glass of water' -> (glass)-[prep_of]->(water). The following dependency tags are otherwise ignored: 'dep', 'det', 'punct', 'pobj', 'ROOT', 'prep', 'cc'

### 2_vocab
Transform the resulting triples into word-context pairs, where the 'context' is the concatenation of the dependency tag and child or parent token, with '-1' appended to denote child->parent directionality. "Words" here will additionally include string concatenated dependency paths with 'subject' and 'object' children as if they were themselves transitive verbs. For example

&emsp;*"Alice is the queen of Antarctica."*

would yield the 2-hop triples:

&emsp;*(be_queen_of)-[nsubj]->(alice)*</br>
&emsp;*(be_queen_of)-[dobj]->(antarctica)*</br>

which are represented bidirectionally as (word, context) pairs:

&emsp;*be_queen_of, alice/nsubj*</br>
&emsp;*be_queen_of, antarctica/dobj*</br>
&emsp;*alice, be_queen_of/nsubj-1*</br>
&emsp;*antarctica, be_queen_of/dobj-1*</br>

These are in addition to the word-context pairs for the significant 1-hop dependency paths
### 3_path2vec

## Inspecting Model Outputs
There is a helper notebook to load a saved state_dict and inspect nearest
neighbors for a given word or path embedding.
```
model.most_similar('move-to')
[('move-to', 1.0),
 ('move-from', 0.8306348919868469),
 ('relocate-to', 0.8269246220588684),
 ('settle-in', 0.8055340051651001),
 ('move-into', 0.7868099212646484),
 ('return-to', 0.7832087278366089),
 ('transfer-to', 0.7795233726501465),
 ('leave-for', 0.7774271965026855),
 ('reside-in', 0.7711591124534607),
 ('travel-to', 0.768322229385376)]

model.most_similar('be_president_of')
[('be_president_of', 0.9999999403953552),
 ('be_chairman_of', 0.8024470806121826),
 ('be_chair_of', 0.764552891254425),
 ('be_manager_of', 0.7625577449798584),
 ('be_founder_of', 0.7623101472854614),
 ('be_director_of', 0.7604293823242188),
 ('be_ceo_of', 0.7582588791847229),
 ('be_member_of', 0.7575125694274902),
 ('appos_chairman_of', 0.7554025650024414),
 ('work-at', 0.7434799075126648)]
```
