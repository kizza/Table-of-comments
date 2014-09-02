# Table of comments

A [Sublime Text 2 & 3](http://www.sublimetext.com) plugin that lets you quick-jump between headings within your comments and optionally creates a table of contents within your document

![demo](http://imgur.com/03V7JGy.gif)

Simply press your binded keystroke then begin typing to quick-jump between the sections of your document.
Not only does it help you navigate your code quickly with custom headings, it keeps you mindful of the overall structure.

### Configuration

By default titles are represented by ">" but each title prefix can be customised via the settings.

/*
* > Heading 1
*
* >> Heading 2
*
* >>> Heading 3
*/

### Running the plugin

It is recommended to run the plugin via a keybinding so that you can press that keybinding and start typing

1. Add a keystroke binding within your preferences (recommended)
   Open "Preferenes -> Key Bindings - User" from the main menu then paste

   { "keys": ["f1"], "command": "table_of_comments" }

2. You can also run the plugin via the command palette (Crtl+ Shift + P). Simply find and run "Table of Comments: Show"


### Outputting a table of contents

You may optionally have a list of the headings maintained within your document by placing "TOC" within a comment anywhere within the document.

For example placing...

/* TOC */

Anywhere in your document will automatically update this comment to reflect the headings in your document.

/*
* TOC
*
* Heading 1
*  - Heading 2
*  -- Heading 3
*/