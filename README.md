# TEITransformer

The main goal of this package is to develop an algorithm of conversion TEI XML into Edition Formats (HTML, DOCX, JSON). 

The algorithm consists of two main parts: 
  
  * an algorithm for converting TEI XML to a format (TEITransformer);
  * a front and back application architecture for creating a digital publication and integrating it into an application or website (https://github.com/Stoneberry/tei_platform.git). 

The client interface is implemented by the ```TEITransformer``` class. The user interacts with the algorithm only using this module. When initializing the object, the user must specify the <b>scenario</b> according to which the transformation will take place. 

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

## Modules

Before proceeding to the description of the templates, it is important to define the TEI infrastructure. The organization of the elements is based on a modular system. Elements that occur under the same conditions are combined into a single module. For example, the drama module describes elements for dramatic text encoding. It is convenient when forming your own TEI vocabulary. You can easily select the necessary elements depending on the specifics and subject matter of your documents.

A similar system was created for the current algorithm. For each of the selected scenarios, lists of core elements were compiled based on the TEI Guidelines and organized into separate files by modules. Then, a document for connecting these modules was created. The user can independently determine which modules to use. By default, the modules that are specific to the scenario are connected. The overall system goes as follows:




## Quickstart

There are only two methods available in the class: 

* load_tei()
* transform() 

First, you need to load the data using the ```load_tei``` method. The function receives the path to the TEI XML file and the path to the schema as input. 


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


## Documentation



