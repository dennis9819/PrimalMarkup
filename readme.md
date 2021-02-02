     ____       _                 _ __  __            _                
    |  _ \ _ __(_)_ __ ___   __ _| |  \/  | __ _ _ __| | ___   _ _ __  
    | |_) | '__| | '_ ` _ \ / _` | | |\/| |/ _` | '__| |/ / | | | '_ \ 
    |  __/| |  | | | | | | | (_| | | |  | | (_| | |  |   <| |_| | |_) |
    |_|   |_|  |_|_| |_| |_|\__,_|_|_|  |_|\__,_|_|  |_|\_\\__,_| .__/ 
                                                                |_|    
# PrimalMarkup

The name already implies everything. PrimalMarkup is probably the worst Markup-Language out there. Please do yourself a favor and don't look at the source-code. This project has been done in a hurry!

PrimalMarkupScript was originally designed to easily add a content table and chapter-numbers to text files. This is achieved by 'compiling' .pms (Primal-Markup-Script-File) into plain text files. Chapter-numbering and indentation as well as generating the table of contents is handled by the compiler.

As of now, the compiler supports two levels of headlines.

# Files

PrimalMarkupScript uses the .pms extension for its sourcefiles. The Repository also contains the complementary VS-Code plugin for syntax highlighting.
Temporary files are created in /tmp and have the suffix .pmc1

## Syntax

The PrimalMarkupScript-Language conatins three basic elements:

 - Comments (of course...)
 - Metadata Tags
 - Content-Tags
 
 ### Comments
 Comments are single-lined and start with `%% `. Inline Comments are not supported.
 It is recommended to remove any preceding white-spaces to avoid bugs. 

### Metadata Tags
Metadata Tags set options for the current scope. Right now,there is only one scope available:

 - Document
 
 All Meta-Tags for the Document-Scope have to be at the beginning of the file.
 The snytax is: `[[gmu.\<option\>=\<value\>]]`
 Valid values are:
|Option|Default|Function|Required|
|--|--|--|--|
| defaultWidth | 80 | Width of the seperator | no |
| spacerChar | '#' | Char used for generating the seperators | no |
| indentation | '\\t' | Char/String used to indent the sub-chapters | no |
| title | | Document title | yes |
| shorttitle | | Short title for generating the ASCII-Art | no |
| author | | Document author | yes |

Example:

    [[gmu.title=Testdokument]]
    [[gmu.shorttitle=Ansible]]
    [[gmu.author=Dennis Gunia]]
    %% Dies ist ein Kommentar. Einfach ignorieren ....
    
### Content Tags
Metadata Tags are substituted by the compiler.  
 The snytax is: `{{gmu.\<option\>(=\<value\>)}}`
 Value is only required by section and subsection.
 
 Valid values are:
 

 - header
 - contents
 - seperator
 - section
 - subsection
#### header
The **header** generates an ASCII-Art banner with the author and title.
Example:

    {{gmu.header}}
 
 Output:
 

        _              _ _     _      
       / \   _ __  ___(_) |__ | | ___ 
      / _ \ | '_ \/ __| | '_ \| |/ _ \
     / ___ \| | | \__ \ | |_) | |  __/
    /_/   \_\_| |_|___/_|_.__/|_|\___|
                                      
    Title   :   Testdokument
    Author  :   Dennis Gunia
    
The ASCII-Text is defined by `gmu.shorttitle`, the Title is defined by `gmu.title` and the Author is defined by `gmu.author`.

#### contents
The content-tag is replaced with the generated table of contents
Example:

    {{gmu.contents}}

 Output:

    1. Kapitel1
    -----------
    	1.1 Hier gehts weiter
    	1.2 Hier gehts weiter Pt. 2
    
    2. Kapitel2
    -----------
    
    3. Kapitel3
    -----------
    	3.1 Hier gehts weiter Pt. 2

#### seperator
The seperator generates a bar with the symbol specified in `gmu.spacerChar` and a width of `gmu.defaultWidth`.

Example:

    {{gmu.seperator}}

 Output:
 

    ################################################################################

#### section
The section tag generates a new chapter and automatically assigns a chapter number.

Example:

    {{gmu.section=Kapitel1}}

Output:

    1. Kapitel1
    ===========

#### subsection
The subsection tag generates a new sub-chapter and automatically assigns a sub-chapter number.

Example:

    {{gmu.subsection=Hier gehts weiter}}

Output:

	1.1 Hier gehts weiter
	---------------------
## Prerequisite

    python3.7 -m pip install pyfiglet 


