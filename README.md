# pycvmaker

Tool to create a pdf out of yaml descriptions. Generates a HTML out of yaml file using Jinja2 and then writes out a pdf of this. I use this to create my cv.

## Why?

* Easy to layout using plain HTML & CSS. No need to mess with Word, Latex or anything like that
* Simple to update content, just maintain a flat YAML file
* YAML is human reader friendly

## Installation

1. Clone rep
2. Rename `templates/entries.sample.yaml` to `templates/entries.yaml` and `templates/settings.sample.yaml` to `templates/settings.yaml`
3. Install requirements (using virtualenv)
4. `cd pycvmaker/pycvmaker` and run script via `python run.py`
The pdf will be created under the `out` folder.

## Configure

In `templates/settings.yaml` are following settings configurable:

Setting|Default|Explanation
-------|-------|-------
cv_template|cv.html|The html template
output_folder|out|The folder of the pdf output
file_name|cv-%Y.%m|The file name pattern, allowing dateformat variables

## How it works

It parses a YAML file (`templates/entries.yaml`) which are then available in the Jinja template as `entries`. Have a look at `templates/cv.html` to see how they are used.


