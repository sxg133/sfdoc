SFDoc
=====

Author: Sahil Grover

Date:   2013-02-13

An apex code documentation generator for Salesforce

Documentation
-------------

### Overview

Generate static HTML files from Salesforce project classes.

Execute:

    python sfdoc.py <source_directory> <target_directory> [--pattern] [--name]

The source directory should be the "classes" directory, and the target directory is the location where the static HTML files will be created.

Classes post-fixed with "Test" (*Test.cls) are ignored.

#### Optional Flags

*    --pattern

     Specifiy which classes to pull from the directory using a pattern (e.g. MyPrefix*.cls)

*    --name

     The title of the project that will appear at the top of each page.

