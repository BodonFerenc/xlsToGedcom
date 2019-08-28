# Excel to Gedcom converter

Excel is one input format of the free, open source family tree software available at http://freshmeat.sourceforge.net/projects/familytree_cgi/ . The expected columns are descried in the documentation and copied below as reference.

Script that is available in this project converts excel to [GEDCOM](https://en.wikipedia.org/wiki/GEDCOM) format which is the de facto standard for genealogy projects like [Gramps](https://gramps-project.org/).

Usage of the script.
The script expects four parameters
   * the excel file name
   * directory in which the pictores of the family members are located
   * the submitter first name
   * the submitter last name
   
Submitter, which is the genealogy data generator person, is mandatory in Gedcom files. The script prints the Gedcom content to the standard output so you can redirect it to any file. Example usage:
```
python xlsToGedcom myFamily.xls Homer Simpson > myFamily.ged
```





Expected excel format as per readme.txt of project [familytree](http://freshmeat.sourceforge.net/projects/familytree_cgi/):

The excel format is quite straightforward based on the example file. Each row (except the header) represents a person. The fields are:
 * ID: the ID of the person. It can be anything (like 123 or Bart_Simpson), but it should only contain alphanumeric characters and underscore (no whitespace is allowed).
 * title: like: Dr., Prof.
 * prefix: like: sir
 * first name
 * middle name 
 * last Name
 * suffix: like: VIII
 * nickname
 * father's ID
 * mother's ID
 * email
 * webpage
 * date of birth: the format is day/month/year, like: 24/3/1977
 * date of death: the format is day/month/year, like: 24/3/1977
 * gender: 0 for male, 1 female
 * is living?: 0 for live 1 for dead
 * place of birth: the format is: "country" "city". The city part may be omitted. Quotation marks are mandatory.
 * place of death: the format is: "country" "city". The city part may be omitted. Quotation marks are mandatory.
 * cemetery: the format is: "country" "city" "cemetery", like: "USA" "Washington D.C." "Arlington National Cemetery"
 * schools: use comma as separator, like: Harward, MIT
 * jobs: use comma as separator
 * work places: use comma as separator
 * places of living: places separated by comma, like: "USA" "Springfield", "USA" "Connecticut"
 * general: you would typically write something general about the person.
Note, that the extension of an excel data file must be xls.

Tip: Select the second row, click on menu Window and select Freeze Panels.
This will freeze the first row and you can see the title of columns.

NAME OF THE PICTURE:

One picture may belong to each person. The name of the picture file reflects the person it belongs to. The picture file is obtained from the lowercased full name by substituting spaces with underscores and adding the file extension to it. From example from "Ferenc Bodon3" we get "ferenc_bodon3.jpg".
