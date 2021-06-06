# TEITransformer

The main goal of this package is to develop an algorithm of conversion TEI XML into Edition Formats (HTML, DOCX, JSON). 

The algorithm consists of two main parts: 
  
  * an algorithm for converting TEI XML to a format (TEITransformer);
  * a front and back application architecture for creating a digital publication and integrating it into an application or website (https://github.com/Stoneberry/tei_platform.git). 

The client interface is implemented by the ```TEITransformer``` class. The user interacts with the algorithm only using this module. When initializing the object, the user must specify the <b>scenario</b> according to which the transformation will take place. 

The algorithm for enabling visualization uses a set of XSLT stylesheets.

<b>XSLT</b> stands for the Extensible Stylesheet Language for Transformations. The main idea is to describe the template of the output document and fill it with the extracted information from XML. The extracting process is conducted by writing rules that specify which element should be converted and under what condition.

## Quickstart

You can install package from PyPi website:

```
pip install TEItransformer
````

There are only two methods available in the class: 

* load_tei()
* transform() 

First, you need to load the data using the ```load_tei``` method. The function receives the path to the TEI XML file and the path to the schema as input. 

### HTML

```
from tei_transformer import TEITransformer


tei_path = "filename.xml"
schema_path = "schema.rng"

TT = TEITransformer(scenario='drama')
TT.load_tei(tei_path, schema_path=schema_path)
TT.transform(
  output_format='html',
  keep_all=False,
  full_page=True,
  enable_valid=False
)
```


### DOCX

```
from tei_transformer import TEITransformer


tei_path = "filename.xml"
schema_path = "schema.rng"

TT = TEITransformer(scenario='drama')
TT.load_tei(tei_path, schema_path=schema_path)
TT.transform(
  output_format='docx',
  modules=[],
  keep_all=False,
  enable_valid=False,
  output_filename='output',
  odd_path=None,
  custom_css_path=None)
```

### JSON

```
from tei_transformer import TEITransformer


tei_path = "filename.xml"
schema_path = "schema.rng"

TT = TEITransformer(scenario='drama')
TT.load_tei(tei_path, schema_path=schema_path)
TT.transform(
  output_format='json',
  enable_valid=False,
  output_filename="output",
)
```


## Scenario

The concept of a scenario is key in the current algorithm. TEI allows you to describe different types of sources. It could be dramatic texts or linguistic corpora, for example. Each of these types differs not only in its purpose, but also in its structure and presentation. In order to take these features into account and create the most suitable output product, transformation and stylization rules have been defined for several data types. 

At the moment, the algorithm has two scenarios: 

* drama
* plain
  
### drama

<i>Drama</i> is a scenario that describes performance texts. Based on the Guidelines, the main elements of the dramatic texts characteristic were collected and their behavior in XSLT templates and styles was determined.

### plain

<i>Plain</i> is a simple format that has no predefined structure. It was created specifically so that the users could determine their own settings of the output.
The <i>plain</i> format is selected as a default value. 

## Complete vs Selective template

The templates are further divided into two subcategories: 

* complete 
* selective 

Complete template allows users to convert XML file to HTML while preserving the entire structure of the document. The only changes are that:

* all internal nodes are saved in the <b>div</b> tag;
* all leaf nodes with text are saved in the <b>p</b> tag;
* the node name becomes a class name. 

TEI:
  
![tei](https://github.com/Stoneberry/TEITransformer/blob/main/static/tei_structure.png)
  
HTML:
 
![html](https://github.com/Stoneberry/TEITransformer/blob/main/static/html_structure.png)
  
A selective template also preserves the overall structure of the document. However, the text is saved for pre-selected items only. The main idea is to create a standardized representation without unnecessary elements. 

![html](https://github.com/Stoneberry/TEITransformer/blob/main/static/selective.png)

## Modules

Before proceeding to the description of the templates, it is important to define the TEI infrastructure. The organization of the elements is based on a modular system. Elements that occur under the same conditions are combined into a single module. For example, the drama module describes elements for dramatic text encoding. It is convenient when forming your own TEI vocabulary. You can easily select the necessary elements depending on the specifics and subject matter of your documents.

A similar system was created for the current algorithm. For each of the selected scenarios, lists of core elements were compiled based on the TEI Guidelines and organized into separate files by modules. Then, a document for connecting these modules was created. The user can independently determine which modules to use. By default, the modules that are specific to the scenario are connected. The overall system goes as follows:

![modular_system](https://github.com/Stoneberry/TEITransformer/blob/main/static/modular.png)


Elements considered in modules:

module | elements
--- | ---
drama elements | titleStmt, author, castItem, castItem, castGroup, roleDesc, role, actor, camera, sound, caption, tech, view, set, set, set, pb, sp, speaker, sp, div[@type='act'], div[@type='scene'], castGroup, castList, head, div[@type='scene'], sp, sp, sp, sp, stage, titleStmt
verse elements | l, lg


## Output 

As mentioned earlier, the program supports 3 output formats: HTML, DOCX, and JSON. 
Each of the formats is created by a separate class that has its own settings. 

### HTML output 

<b>Arguments:</b>

argument | data type | description
--- | --- | ---
module | list | list of module names to include in the transformation process
keep_all | bool | whether to keep all data (True) or select only modular ones (False)
output_filename | str | output file path
odd_path | str | odd file path
custom_css_path | str | css file path
links | bool | whether to include link processing or not
full_page | bool | whether to create a full interface representation (True) or not (False)
enable_valid | bool | whether to consider validity obligatory for transformation


The user can also select one of the following output formats:

* a simple text representation which includes the text of the document stylized in accordance with predefined styles (whether by the user or default settings);
* a standalone responsive text viewer interface.

The standalone interface includes features such as:

* increasing/decreasing the text size
* file description
* automatically generated document content 
* search engine. 

The document also consists of an HTML structure and CSS code for stylization. However, it also requires JavaScript (JS) code for interactive work with the page. The autonomy of the file is provided by the fact that all the additional code is included in the document. Since it is just one file, it can easily be used not only for personal browsing but also to be shared with others or embedded in any resource.


![full_page](https://github.com/Stoneberry/TEITransformer/blob/main/static/full_page.png)

* 1 — collapsible sidebar with the content of the document; 
* 2 — text size increasing/decreasing buttons; 
* 3 — pop-up file description window; 
* 4 — pop-up search engine window; 
* 5 — link to the author's wikipedia page. 


#### File description

The formation of the description and content of the document requires an analysis of its structure. According to the guidelines of the default text structure any bibliographical description about the file should be stored inside the <b>fileDesc</b> tag (TEI Consortium. n.d., f). Thus, the program extracts all the data from the tag and presents it in the pop-up file description window (see Figure 7).
  
#### Document content

As for document content generation, the algorithm searches for the <b>head</b> element. Despite the fact that the <b>head</b> tag most often indicates the beginning of a new section. It can also be part of lower-level elements. Therefore, the user needs to define the behavior of the tag in the ODD file for better document processing. 
  
#### Search

There are two types of search in:

* content
* structure of the document. 

##### Content

The program extracts all text elements from the document, divides them into sentences, and finds matches with the user's query using a fuzzy string searching algorithm. 

##### Structure

The structure is searched using XPATH. The user is prompted to enter a string with XPATH expressions to select nodes. This is possible due to the preservation of the document structure at the stage of transformation of XML to HTML. The only exception is that the tag names are converted to classes. Accordingly, to find all the phrases of a certain character the expressions ```.sp[who=“character_name”]``` should be used instead of ```sp[who=“character_name”]```, where the dot denotes that the pursuing sequence is a class name. It is also possible to save the search results in a txt file.


#### Links

In addition, the program considers several types of links during the analysis process:

* links defined by the @ref attribute; 
* links decorated in nodes specified with the attribute @type “URL” or “UTI”; 
* Wikidata ID decorated in nodes specified with the attribute @type “wikidata”;
* Wikidata ID references in @key attribute in form of “wikidata:Q729569”



### DOCX output 

<b>Arguments:</b>

argument | data type | description
--- | --- | ---
module | list | list of module names to include in the transformation process
keep_all | bool | whether to keep all data (True) or select only modular ones (False)
output_filename | str | output file path
odd_path | str | odd file path
custom_css_path | str | css file path
enable_valid | bool | whether to consider validity obligatory for transformation

DOCX styling is limited to the following methods:

* text alignment;
* indent the first line of text;
* adjusting the line spacing;
* changing font characters: weight, size, color and style;
* color can be specified only with RGB notation;
* size cab be specified only in <i>cm</i>, <i>pt</i> or <i>in</i>

Another limitation is that all styles are applied only to the paragraph, i.e. text elements. Accordingly, to add margins, for example, you need to specify the appropriate style not for the block as a whole, but for its last element or for the first element of the next block.


### JSON output 

<b>Arguments:</b>

argument | data type | description
--- | --- | ---
output_filename | str | output file path
enable_valid | bool | whether to consider validity obligatory for transformation

The transformation to the JSON format occurs by traversing all the elements of the XML tree. Each node in the tree is examined for the presence of descendants. If no children are found, the node is perceived as a leaf node. Each node is presented as a dictionary of 2 primary parameters: attributes and value. For internal nodes, the children list parameter is also defined. The choice of presenting children in the form of a list, rather than a dictionary, is due to the possibility of the presence of several tags of the same name in the structure. Everything is stored in a Python dictionary and then converted to JSON. The resulting structure goes as follows:

```
{node_name:
  {value: “”, 
   attrs: {id: “node1”},
   children: [
      {“children1”: {...}},
      {“children2”: {...}}
      ]
 }
```

## Stylization

For each of the scenarios its own stylesheet was defined. The display rules were determined based on the typesetting standards.

Users can also specify their own rules by providing a path to the CSS file. In this case, the program analyzes the user's data and compares it with the default sheets. There are three possible cases:

* the user defined rule set for a tag that is not specified in the default styles;
* the user defined a not specified rule for an existing tag in the default styles;
* the user defined an already specified rule for an existing tag in the default styles.

In the first case, the entire rule set is added to the style constructor. In the second case, the program adds a new rule to the existing set of rules. Finally, the program replaces the existing rule with a new one.

Due to the fact that at the transformation stage, the tag names become the name of the class. It is important that the user uses class notation when defining rules for tags. 


## Customization

ODD is used for allowing the user to customize the output of the algorithm in question. Since ODD is based on XML, the user does not need to have additional knowledge like XSLT to adjust the transformation behavior. 

However, for now, this ability is limited to the processing of several types of tag behaviour with the <model> tag. A single element can be specified with the <elementSpec> tag. The <model> tag, as a part of <elementSpec>, documents the rules for the node rendering. For example, CSS style name identification through a @cssClass attribute or predefined function name selection through @behaviour attribute. In the present paper, I consider only two following functions of @behaviour attribute: omit mode to ignore the element and heading mode to view the element as part of a document content. The program also takes into account conditions in which the element occurs via @predicate attribute. Nevertheless, it is worth mentioning that the CSS is sufficient to implement most of the behaviour functions. For instance, line display: none can remove an item from the document.

