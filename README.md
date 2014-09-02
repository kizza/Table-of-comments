# Table of comments

A [Sublime Text 2 & 3](http://www.sublimetext.com) plugin that lets you quick-jump between headings within your comments and optionally creates a table of contents within your document

![demo](http://imgur.com/uIhsQ8A.gif)

Run the plygun (via a keystroke) to open the quick-jump panel and begin typing to easily navigate between  sections of your document. Not only does it help you navigate your code quickly with custom headings, it keeps you mindful of the overall structure of your document..

### How to use it

Simply start using headings within your comments to organise your document.
By default titles are represented by ">" but each title prefix can be customised via the settings.

```
/*
* > Heading 1
*
* >> Heading 2
*
* >>> Heading 3
*/
```

### Running the plugin

It is easiest to run the plugin via a keybinding so that you can open the quick-jump menu, start typing and easily navigate around your document

1. Add a keystroke binding within your preferences (recommended)
   Open "Preferenes -> Key Bindings - User" from the main menu then paste

   ```{ "keys": ["f1"], "command": "table_of_comments" }```
   
   (This runs the plugin by pressing F1)
   
2. You can also run the plugin via the command palette (Crtl+ Shift + P). Simply find and run "Table of Comments: Show"


### Outputting a table of contents

You can optionally output a list of the headings within your document by placing "TOC" within a comment anywhere within the document.

For example placing...

```/* TOC */```

Anywhere in your document will automatically update to reflect the headings in your document when you open the quick-jump panel (ie. run the plugin)

```
/*
* TOC
*
* Heading 1
*  - Heading 2
*  -- Heading 3
*/
```

(You can the title for each table of contents within the plugin settings.  For example if changed to "Within this document" simply place that text within a comment in your document to have the table of content maintained with that title.
