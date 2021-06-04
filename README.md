# TEITransformer

The main goal of this package is to develop an algorithm of conversion TEI XML into Edition Formats (HTML, DOCX, JSON). The algorithm consists of two main parts: an algorithm for converting TEI XML to a format (TEITransformer) and a front and back application architecture for creating a digital publication and integrating it into an application or website (TEITransformer: https://github.com/Stoneberry/tei_platform.git). 

The client interface is implemented by the TEITransformer class. The user interacts with the algorithm only using this module. When initializing the object, the user must specify the scenario according to which the transformation will take place. The plain format is selected as a default value. 

There are only two methods available in the class: load_tei and transform. First, you need to load the data using the load_tei method. The function receives the path to the TEI XML file and the path to the schema as input. 


## Data
Depending on the specified parameters and the user's needs, the input data may vary. In general, the input data of the algorithm can be divided into two types: user files and program settings. 

The user files can include the electronic text document itself, preferably, designed according to the TEI Guidelines; XML schema, if a custom notation system is used; ODD or CSS files for the output customization. XML schema, validation, and customization processes will be described in more detail in the following sections. 
The program settings include the output format and XSLT conversion settings. One example of the latter is the scenario parameter. The concept of a scenario is key in the current algorithm. TEI allows you to describe different types of sources. It could be dramatic texts or linguistic corpora, for example. Each of these types differs not only in its purpose, but also in its structure and presentation. In order to take these features into account and create the most suitable output product, transformation and stylization rules have been defined for several data types. 
At the moment, the algorithm has two scenarios: drama and plain. Drama is a scenario that describes performance texts. Based on the Guidelines, the main elements of the dramatic texts characteristic were collected and their behavior in XSLT templates and styles was determined. Plain is a simple format that has no predefined structure. It was created specifically so that the users could determine their own settings of the output.
Another parameter is the completeness of the tags considered. There are two options for analysis: the program selects only those tags that are defined for a particular thematic scenario or saves all the tags specified in the file. The first option was designed to regulate the information that the user wants to display. Texts may contain different sorts of meta-information which may not be desirable for publication purposes. 


## Quickstart

```
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
