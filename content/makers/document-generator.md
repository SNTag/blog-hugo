---
title: "Document Generator"
author: "SNTag"
date: "2024-03-26T00:00:00Z"
layout: post
summary:
    "**Makers file**: My method to document creation using Pandoc and makefiles into presentations (beamer) or pdfs."
categories:
  - blog
  - Makers
  - makefile
  - pandoc
  - beamer
  - latex
  - markdown
  - md
  - pdf
  - linux
---


-   [Overview](#overview){#toc-overview}
    -   [Setup/Install](#setupinstall){#toc-setupinstall}
    -   [Sites to go through for
        details:](#sites-to-go-through-for-details){#toc-sites-to-go-through-for-details}
    -   [TO SOLVE FOR EASIER DOCUMENT
        MAKING](#to-solve-for-easier-document-making){#toc-to-solve-for-easier-document-making}
    -   [My Makefile General
        Guide](#my-makefile-general-guide){#toc-my-makefile-general-guide}
    -   [To develop](#to-develop){#toc-to-develop}
    -   [Autostart sh](#autostart-sh){#toc-autostart-sh}
-   [PDF](#pdf){#toc-pdf}
    -   [Future
        developments](#future-developments){#toc-future-developments}
-   [Presentations](#presentations){#toc-presentations}
    -   [Makefile (Mar 26th,
        2024)](#makefile-mar-26th-2024){#toc-makefile-mar-26th-2024}
    -   [How To](#how-to){#toc-how-to}

:title: Document Generator

# Overview

This document is a summary of my document making process in markdown \>
latex \> document. Setup on linux, pop~os~!

Requires:

-   latex
-   pandoc

[Great pandoc guide](https://pandoc.org/MANUAL.html) [Pandoc
manual](https://pandoc.org/MANUAL)

## Setup/Install

### Texlive or Latex

To install, run \`sudo apt install -y texlive texlive-full\`

NOTE: texlive-full gets stuck at \'Pregenerating ConTeXt MarkIV
format\'. Solved by letting it run for a while, and then pressing
\"Enter\" a whole lot, as mentioned by one user online.

### Pandoc

Make sure to install at the same version as
[pandoc-crossref](https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.17.0e).
See [here](https://github.com/jgm/pandoc/blob/main/INSTALL.md#linux) for
installation (run dpkg -i on [downloads
page](https://github.com/jgm/pandoc/releases) dpkg release).

Extra note: handy to remove tags in url to find packages by version.

1.  pandoc-crossref

    Make sure to install at the same version as
    [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref/releases).

    Place pandoc-crossref in \`\~/.local/bin/\` & then restart. In
    \`echo \$PATH\`, pandoc-crossref placed in \~/.local/bin will not
    show until restart.

## Sites to go through for details:

<https://alvinalexander.com/blog/post/latex/reference-figure-or-table-within-latex-document/>
Nicely comprehensive:
<https://opensource.com/article/18/9/pandoc-research-paper>
<https://boisgera.github.io/pandoc/markdown/>
<https://blog.cubieserver.de/2021/document-writing-with-markdown-and-latex/>
<https://allefeld.github.io/nerd-notes/Markdown/A%20writer's%20guide%20to%20Pandoc's%20Markdown.html>
Nice list of features:
<https://deatrich.github.io/doc-with-pandoc-markdown/current/doc-with-pandoc-markdown.html#fenced-code-blocks>

## TO SOLVE FOR EASIER DOCUMENT MAKING

### \[#B\] alt txt font size

I suspect best option is not to use markdown approach but latex or html

### \[#B\] MAKEFILE: Edits for handouts & regular slides?

<https://gist.github.com/lmullen/c3d4c7883f081ed8692a#file-makefile>

## My Makefile General Guide

### Start

Location for texlive documents is /usr/share/texlive when \`sudo apt
install texlive-full\`

### Declaring Documents to Use

### File Types to Generate

Guide: -r input format.
[-s](https://pandoc.org/MANUAL#option--standalone) Produce output with
an appropriate header and footer. -V specifics a theme already in the
system. Needs --template for personal theme. -t output format.
\$(FILTERS) after --pdf-engine. --csl=\$(CSL).csl --bibliography=\$(BIB)
-N --reference-doc Use with pptx templates
\[\[[https://pandoc.org/MANUAL#option\--toc\\](https://pandoc.org/MANUAL#option--toc\)\[\]\[--toc\]\]
Table of Contents. Useless without the -s option

### To Put Together The Finale Document

## To develop

### To put columns?

[pandoc manual](https://pandoc.org/MANUAL.html#columns)

### \[#C\] spelling

yaml header: \"spellchecker: hunspell\" lua-filter=spellcheck

### \[#C\] Figure out bib (NEEDS PANDOC-CROSSREF?)

### \[#A\] PANDOC: crossref

-   <https://emacs.stackexchange.com/questions/35775/how-to-kill-magit-diffs-buffers-on-quit>

### \[#A\] PDF: Figures prefix/reference using markdown syntax (NEEDS PANDOC-CROSSREF?)

Following seems specific to document making with markdown syntax. Needs
pandoc-crossref? [see stackoverflow
response](https://stackoverflow.com/questions/9434536/how-do-i-make-a-reference-to-a-figure-in-markdown-using-pandoc)
[blog post focusing on markdown syntax in a
paper](https://opensource.com/article/18/9/pandoc-research-paper)

``` yaml
figPrefix:
 - "Figure"
 - "Figures"

tblPrefix:
 - "Table"
 - "Tables"
```

using md syntax, add \`{#fig:scatter-matrix}\` to end of figure. Ref
using

### \[#C\] PDF: Controlling image location

## Autostart sh

This script is run on a terminal from the directory with the files. auto
runs \'make\' based on changes to the directory.

    #!/bin/bash

    # Automatically set WATCH_DIR to the directory where this script is located
    SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
    WATCH_DIR="${SCRIPT_DIR}" # Directory to watch for changes
    MEXT="(md|yaml)" # Markdown file extension
    SLEEPTIME=1 # Sleep time between checks in seconds

    # Function to compile documents
    compile_docs() {
        echo "Detected changes. Compiling documents..."
        make all
        echo "Compilation finished."
    }

    # Function to clean generated documents
    clean_docs() {
        echo "Cleaning up generated documents..."
        make clean
        echo "Cleanup finished."
    }

    # Initial clean and compile
    clean_docs
    compile_docs

    # Get the initial state of the directory
    initial_state=$(ls -lR --time-style=full-iso $WATCH_DIR | grep -E "\.$MEXT")

    echo "Watching for changes in $WATCH_DIR. Press [CTRL+C] to stop."

    # Continuous loop to check for changes
    while true; do
        sleep $SLEEPTIME
        current_state=$(ls -lR --time-style=full-iso $WATCH_DIR | grep -E "\.$MEXT")

        # Check if anything changed
        if [ "$initial_state" != "$current_state" ]; then
            compile_docs
            initial_state=$current_state
        fi
    done

# PDF

## Future developments

### [Tuft handouts](https://quarto-dev.github.io/quarto-gallery/page-layout/tufte.html)

# Presentations

## Makefile (Mar 26th, 2024)

This is the makefile used to generate the document.

    ## Put this Makefile in your project directory---i.e., the directory
    ## containing the paper you are writing. Assuming you are using the
    ## rest of the toolchain here, you can use it to create .html, .tex,
    ## and .pdf output files (complete with bibliography, if present) from
    ## your markdown file.
    ## -    Change the paths at the top of the file as needed.
    ## -    Using `make` without arguments will generate html, tex, and pdf
    ##  output files from all of the files with the designated markdown
    ##  extension. The default is `.md` but you can change this.
    ## -    You can specify an output format with `make tex`, `make pdf`,
    ## -    `make html`, or `make docx`.
    ## -    Doing `make clean` will remove all the .tex, .html, .pdf, and .docx files
    ##  in your working directory. Make sure you do not have files in these
    ##  formats that you want to keep!

    ## IMPORTANT TODO
    # [B] Two column slides, one with image? Adjusting width of columns
    # [C] Figure out bib
    # [D] What is 'submission'?

    ## Later things to learn
    # What are slide levels, ex pandoc --slide-level 2
    # Confirm what pandoc --toc does
    # Possible to tell markdown to exclude titles?

    OS := $(shell uname)

    ## Markdown extension (e.g. md, markdown, mdown).
    MEXT = md

    ## All markdown files in the working directory
    SRC = $(wildcard *.$(MEXT))

    ## Final doc
    # This is a document that will be generated containing the sum.
    FINAL_DOC := final_doc.md

    ## Location of Pandoc support files.
    PREFIX = ${HOME}/.config/pandoc/

    ## Location of parent bibliography
    #LIBRARY=library.bib # TODO Will this function with this line included, as well as the below bib mentions?

    ## Location of your working bibliography file
    # Contains the citations
    #BIB = bibexport.bib

    ## CSL stylesheet (located in the csl folder of the PREFIX directory).
    #CSL = acrf  # For styling of Bibliography # TODO are there CSL stylesheets in texlive/pandoc?

    ## TEMPLATE
    # Location for texlive documents is /usr/share/texlive when `sudo apt install texlive-full`
    TEMPLATE    =   metropolis  # TODO where does it search for template? # NOTE Template document.

    PDFS=$(SRC:.md=.pdf)
    TEX=$(SRC:.md=.tex)
    PPTX=$(SRC:.md=.pptx)

    FILTERS = --filter pandoc-crossref # --filter pandoc-citeproc #--lua-filter=draftnotes # TODO any useful lua filters for presentations?

    EXTENSIONS := simple_tables+table_captions+yaml_metadata_block+smart # TODO How are these extensions installed/added?

    ##############################
    # DECLARING DOCUMENTS TO USE #
    ##############################

    SUBMISSION  =   submit/GTK-AcRF-T1-2018.pdf  # TODO Where to save the file?

    PDFENGINE=pdflatex

    # NOTE When Available, add to line below:
    # bibexport.bib $(TEMPLATE).latex $(CSL).csl
    #final_presentation.pdf:    final_presentation.md presentation.md Makefile  # NOTE Files to generate .pdf # TODO Why is Makefile listed here?


    all:    $(PDFS) $(TEX) $(PPTX)

    pdf:    clean $(PDFS)
    tex:    clean $(TEX)
    pptx:   clean $(PPTX)

    # GUIDE:
    # See FINAL_DOC variable above
    # NOTE Change this to arrange order of documents.
    # Used to be grant.md.
    $(FINAL_DOC):   00-metadata.yaml \
        01-presentation.md
        cat $^ >| $@

    ##########################
    # FILE TYPES TO GENERATE #
    ##########################

    # Guide:
    # -r input format.
    # -s enables titles?
    # -V specifics a theme already in the system. Needs --template for personal theme.
    # -t output format.
    # $(FILTERS) after --pdf-engine.
    # --csl=$(CSL).csl
    # --bibliography=$(BIB)
    # -N
    # --reference-doc Use with pptx templates

    %.pdf:  $(FINAL_DOC)
        pandoc -r markdown+$(EXTENSIONS) -t beamer \
        -s --pdf-engine=$(PDFENGINE) \
        $(FILTERS)  \
        -V theme:$(TEMPLATE) \
        -o $@ $<

    %.tex:  $(FINAL_DOC)
        pandoc -r markdown+$(EXTENSIONS) \
        -s --pdf-engine=$(PDFENGINE) \
        $(FILTERS)  \
        -V theme:$(TEMPLATE) \
        -o $@ $<

    # TODO Add  $(FILTERS)  \ to pptx?
    %.pptx: $(FINAL_DOC)
        pandoc -r markdown+$(EXTENSIONS) -s -t pptx \
        -o $@ $<

    clean:
        rm -f *.pdf *.tex *.pptx


    #########################################
    # # TO PUT TOGETHER THE FINALE DOCUMENT #
    #########################################

    # Guide:
    # This segment will combine parts from multiple documents
    # In this setup, it takes the $(GRANT_SHELL) page 1-8, places grant.pdf first 11 pages for 9-19, and back to $(GRANT_SHELL) for 20 onwards.
    # TODO figure out this section

    # $(SUBMISSION): final_presentation.pdf
    #   pdfjam --a4paper $< \
    #        --outfile $@

## How To

### Notes

[stack
overflow](https://stackoverflow.com/questions/44906264/add-speaker-notes-to-beamer-presentations-using-rmarkdown)

Use either `\note{}`{=latex} or ::: note :::

### Figures (LATEX)

Font size follows that in
[here](https://www.overleaf.com/learn/latex/Font_sizes%2C_families%2C_and_styles#Reference_guide)

``` yaml_code
header-includes:
    - \usepackage[font={footnotesize},labelfont=bf]{caption}
```

``` latex_figure
\begin{figure}
    \includegraphics[width=0.5\textwidth,height=\textheight]{./images/EnvelopedmRNA.png}
    \caption{something here}
\end{figure}
```

### Figures (MARKDOWN)

Haven\'t confirmed whether \`#fig\` works in this context

``` md_figure
![alt_text](./image.pnd){ width=50% style="center" #fig:figurelabel }
```
