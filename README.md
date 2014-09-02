# Table of comments

A [Sublime Text 2 & 3](http://www.sublimetext.com) plugin that lets you organise and quick-jump between headings in your comments as well as optionally output a live table of contents too.

![demo](http://imgur.com/uIhsQ8A.gif)

Organise your code with headings within your comments then run the plugin to open the quick-jump panel to easily navigate between sections of your document. Not only does it help you navigate your code quickly with custom headings, it keeps you organised and mindful of the overall structure of your document.

### How to use it

Simply start using headings within comments to organise your code using the format below.
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

### Jumping between titles

It is easiest to run the plugin via a keybinding so that you can open the quick-jump menu quickly whilst typing.

1. Add a keystroke binding within your preferences (recommended)
   Open "Preferenes -> Key Bindings - User" from the main menu then paste

   ```{ "keys": ["f1"], "command": "table_of_comments" }```
   
   (This example runs the plugin by pressing F1)
   
2. You can also run the plugin via the command palette (Crtl+ Shift + P). Simply find and execute "Table of Comments: Show"


### Outputting a table of contents

You can optionally output a maintained list of the headings within your document by placing "TOC" inside a comment anywhere within the document.

For example placing...

```/* TOC */```

...anywhere in your document will automatically it update to reflect the headings in your comments each time you run the plugin.

```
/*
* TOC
*
* Heading 1
*  - Heading 2
*  -- Heading 3
*/
```

(You can change the title for your table of contents within the plugin settings.  For example, you can change "TOC" to be "Within this document", then simply place that text within a comment in your document to have the table of content maintained with that title.)
