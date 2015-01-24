# Table of comments

A [Sublime Text 2 & 3](http://www.sublimetext.com) plugin that lets you organise and
quick-jump between headings in your comments (like "jump to symbol") as well as 
optionally output a live table of contents within your document.

![demo](http://imgur.com/uIhsQ8A.gif)

Organise your code with headings within your comments then run the plugin 
to open the quick-jump panel and easily navigate between sections of your document. 
Not only does it help you navigate your code quickly with custom headings, 
it keeps you organised and mindful of the overall structure of your document.


### How to install

**Via package control**  
Open your command palette -> Package Control: Install Package -> Table of comments

**Manual**

Go to your packages folder(Preferences -> Browse Packages)
```bash
# clone this repo
git clone https://github.com/kizza/Table-of-comments 'Table of comments'
```
Or download the leatest [release](https://github.com/kizza/Table-of-comments/releases) 
and unzip it in a folder named `Table of comments`

### How to use it

Simply start using headings within comments to organise your code using the format below.
By default titles are represented by ">" but each title prefix can be customised via the settings.

```
/*
* > Heading 1
*/
...
/*
* >> Heading 2
*/
...
/*
* >>> Heading 3
*/
```

### Jumping between headings

The easiest way to run the plugin is via a keybinding so that you can open 
the quick-jump menu quickly whilst typing.

1. Add a keystroke binding within your preferences (recommended)
   Open "Preferenes -> Key Bindings - User" from the main menu then paste

   ```{ "keys": ["f1"], "command": "table_of_comments" }```
   
   (This example runs the plugin by pressing F1)
   
2. You can also run the plugin via the command palette (Crtl+ Shift + P). 
Simply find and execute "Table of Comments: Show"

Then just like how you are able to quick-jump between functions and selectors 
you can now jump between the documentation and comment headings within your document.

### Moving up and down through comments

You can also move to the next/prev comment from your local position.
Here are some examples of the keybindings you can set in 
"Preferenes -> Key Bindings - User" from the main menu.

   ```
   { "keys": ["alt+up"],   "command": "table_of_comments", "args":{ "move":"up" } }
   { "keys": ["alt+down"], "command": "table_of_comments", "args":{ "move":"up" } }
   ```
Feel free to set any keyboard shortcuts you like.

(This behaviour inspired by by [Sublime Move By Symbols](https://packagecontrol.io/packages/Move%20By%20Symbols) plugin)


### Outputting a table of contents (optional)

You can optionally output a maintained list of the headings within your document
by placing "TOC" inside a separate comment anywhere within the document.

For example placing...

```/* TOC */```

...anywhere in your document will automatically update it to reflect the headings 
within your comments each time you run the plugin.

```
/*
* TOC
*
* Heading 1
* - Heading 2
* -- Heading 3
* --- Heading 4
*/
```

You can change the title for your table of contents within the plugin settings.  
For example, you can change "TOC" to be "Within this document", then simply place 
that text within a comment in your document to have the table of content maintained 
with that heading.

### Customising the plugin

You can tweak the plugin settings for parsing headings (ie. which characters 
designate each level of headings) as well as for formatting the table of contents output.

To view the existing plugin settings run the command 
"Table of comments: Settings - Default" from the command palette (Ctrl + Shift + P).
Then run "Table of comments: Settings - User" and paste in any of the settings 
you wish to change.

Ultimately the above creates a "tableofcomments.sublime-settings" file in
your "Packages/User" directory.

#### Changing the heading characters

For example you can use colons to designate level headings...

```
/*
* : Heading 1
*
* :: Heading 2
*
* ::: Heading 3
*/
```

By using the setting...

```
"level_char": ":",
```

#### Tweaking the table of comments title

Rather than "TOC" designating the comment to be updated with your table of contents 
you could enter the setting...

```
"toc_title":"Within this document"
```

Which means you can use the comment below to manage your table of contents

```
/* Within this document */
```

#### Only showing first level headings within the table of comments

If you've dilegently organised lots of first, second and third headings within your
document for the purposes of quick-jumping around, it may be too much to display 
them all within the table of comments.

You could of course not include the /* TOC */ comment in your document, or use the 
setting below to only show first level headings.

```
"toc_level":"1"
```
