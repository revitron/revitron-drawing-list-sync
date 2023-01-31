# Drawing List Sync

A Revitron extension that lets you easily synchronize Excel drawinglists to Revit. Parameters and sheets are optionally created automatically.

- [Installation](#installation)
	- [Recommended Installation Methods](#recommended-installation-methods)
	- [Manual Installation](#manual-installation)
- [Sheet Parameter Sync](#sheet-parameter-sync)
	- [Options](#options)
	- [Syncing Data](#syncing-data)
	- [Example Excel File](#example-excel-file)
- [Custom Revision List](#custom-revision-list)
	- [Options](#options-1)
	- [Example](#example)


## Installation

Note that this extensions requires **pyRevit** and **Revitron** to be installed!

### Recommended Installation Methods

In order to use this extension it can either be installed with the [pyRevit CLI](https://www.notion.so/Manage-pyRevit-extensions-fa853768e94240b5b59803e5d7171be3) or using the Revitron [Package Manager](https://revitron-ui.readthedocs.io/en/latest/tools/rpm.html).

### Manual Installation

Alternatively it is also possible to simply clone the repository into the extension directory of pyRevit.

~~~
cd path\to\pyRevit\extensions
git clone https://github.com/revitron/revitron-drawing-list-sync.git revitron-drawing-list-sync.extension
~~~

## Sheet Parameter Sync

The main task of this extension is to update sheet parameters with those saved in a Excel file. It is possible to also automatically create missing sheets and parameters on the fly.

### Options

The behavior of the extensions can be configured by opening the extension settings under `Revitron > DLS > Drawing List Sync > Configuration`. The configuration is stored in the model itself.

| Name | Description |
| ---- | ----------- |
| *Create Missing Sheets* | Check this box in order to create new sheets that exist in the XLS file but not in the Revit model |
| *Create Missing Parameters* | Check this box in order to create new sheet parameters that exist in the XLS file but not in the Revit model |
| *Excel File Path* | The full path to the Excel file |
| *Worksheet Name* | The name of the work sheet |
| *Parameter Name Row Number* | The row number that contains the parameter names to be synced |
| *Sheet Number Parameter* | The name of the parameter that contains the unique sheet number that serves as ID for syncing |

### Syncing Data

In order to actually sync data, first make sure the extension is configured properly as described above. Then simply hit the `Revitron > DLS > Drawing List Sync > Synchronize` button.

### Example Excel File

In the following example, the second row is defined in the configuration to be the parameter row.

|       | A | B | C | ... |
|-------|---|---|---|-----|
| **1** | Some title |
| **2** | *Sheet Number* | *Sheet Name* | *Level* 
| **3** | 1000 | Floorplan | 01 
| **4** | 1010 | Floorplan | 02 
| **5** | 2000 | Section   | XX 

In order to to make a sync work with the Excel file above, set the *Parameter Name Row Number* to 2.

## Custom Revision List

Additionally to just sync sheets parameters, it is also possible to create revision list per sheet, based on a submission matrix in the excel file. Conceptually you just have to define a row that contains sumbission dates and descriptions as shown below and then add a revision index of your choice to any sheet crossing the respective revision column it is submitted on. The revision list will be created in a multiline text parameter and all past revisions as well as the next revision from the day of syncing with be included into that list. Make sure to format the label that shows the list to use a monospace font in order to correctly show the indentation.

### Options

| Name | Description |
| ---- | ----------- |
| *Enable Parsing Revisions* | Enable the revision list feature |
| *Revision Row Number* | The row that is used for revision information. Note that this must not be the same value as *Parameter Name Row Number*. See the example below for how to format revisions. |
| *Revision Text Parameter Name* | The name of the parameter that is created and used to store the revision list |
| *Maximum Index Length* | A formatting option used to calculate a readable indentation for the index |
| *Maximum Date Length* | A formatting option used to calculate a readable indentation for the date |
| *Maximum Title Length* | A formatting option used to calculate a readable indentation for the title |
| *Date Format* | The date format, the default is `%d.%m.%Y` |
| *Maximum Number of Lines* | The maximum number of lines that are created in the revision list |

### Example

|       | A | B | C | ... | H | I | J | K |
|-------|---|---|---|---|---|---|---|---|
| **1** | Some title |
| **2** | Sheet Number | Sheet Name | Level |     |
| **3** |              |            |       |     | 2023-01-09<br>First Submission | 2023-02-15<br>Second Sumbission | 2024-04-01<br>Third One
| **4** | 1000 | Floorplan | 01 |  | A | B | C
| **5** | 1010 | Floorplan | 02 |  |   | A 
| **6** | 2000 | Section   | XX |  |   | A | B
