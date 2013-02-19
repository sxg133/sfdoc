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

*    --verbose

     Verbosity level for console output (0=none, 1=class, 2=method, 3=param).

#### Comment Header Templates

*Class Header Template*

    Class Description

    @author author name1 <author_email1>
    @author author name2 <author_email2>
    @since	yyyy-mm-dd

*Method Header Template*

	Method Description

	@param	param_name1	param description1
	@param	param_name2	param description2

	@return	return description
