---
categories:
- programming
- emacs
- julia
- jupyter
date: "2020-04-13T00:00:00Z"
date-string: April 13, 2020
author: "Shayonendra N. Tagore"
title: Getting Emacs and Julia to work
---

# Julia and Emacs

Julia is a hot upcoming language. I see nothing but support for it online, and many benchmarks showing a notable improvements over Python or R. The main reason why it is not already rivaling Python or R is the framework and packages. The language is still new, and does not have a mature framework. Even though it is now on the stable v1.4, there are features I've seen described as as 'in development'. The packages are also maturing, and I can find many equivalent packages to those I use a biologist. However, I will admit a certain level of distrust until I understand Julia better.

I've been meaning to play with this language, but the biggest obstacle is the IDE. My Emacs config
	is something that I've grown very attached to, and I'm not going to use any other if I have
to. Unfortunately, nearly all of the packages I found for Emacs+Julia have not been worked on for 3 years
or more. I suspect that Emacs support for the language will not be great for a while. The best hope for anyone is to use
ESS, which has active support for Julia.

<!-- https://github.com/gjkerns/ob-julia/blob/master/ob-julia-doc.org) (the guide to julia-org-mode on the website) was last update on 2017. -->

The best implementation of Julia that I have achieved is ESS+Jupyter. This approach has created a
stable environment with all of the features I rely on; autocompletion, access to a shell, access to
documentation. Plus, while org-babel is unavailable, I can add literate notes to my experiments in
Julia!

For anyone interested, a simplified version of my config[^1] is this:

```elisp
;; ====================
;; ess
;;
;; This is a very simplified version of my config.
(use-package ess
  :mode (
         ("\\.jl\\'" . ess-mode)
         ("\\.R\\'"  . ess-mode)
         ("\\.r\\'"  . ess-mode)
	 )
  )

;; ====================
;; julia-mode
;;
;; dependency for the ess-julia-mode-hook
(use-package julia-mode
  :mode ("\\.jl\\'" . ess-mode)
  :init
  (add-hook 'julia-mode-hook 'ess-julia-mode)
  )

;; ====================
;; for ein (jupyter)
(use-package ein
:defer t)

(require 'ein)
(require 'ein-notebook)
(require 'ein-subpackages)
```

When starting the terminal using this approach, you might get the message "Terminal not
functional". According to a [github issue](https://github.com/emacs-ess/ESS/issues/143), the system
is just upset about a missing history file.

As a little extra, Manjaro users may have had issues with downloading packages through Julia. Add this line to your Bashrc/Zshrc, and it should be fixed:

`export JULIA_PKG_SERVER=pkg.julialang.org`

# Summary of this approach
## Positives:
-Adds ESS support to Julia. This adds a large number of features that currently lack from any other competitors.
-Adds jupyter support through [EIN](https://github.com/millejoh/emacs-ipython-notebook), enabling literate programming.
-Source-editing will now have auto-complete for julia.
-Stable enough to get you going!

## negatives:

-No org-mode for now...

If you want to reach out to me about this post, please leave an issue on the [github repo](https://github.com/sntag/sntag.github.io/issues). I will get around to setting up a comments system for a static website eventually.

## discontinued packages for Julia that I had found (in case your interested)

- [Julia-shell](https://github.com/dennisog/julia-shell-mode): seemed promising, but was last updated in 2016 as of writing. That was before the
release of v1. Considering the issues and level of maturity that <v1 Julia had, I'm not keen on
testing this shell's stability.
- [ob-julia](https://github.com/gjkerns/ob-julia/blob/master/ob-julia-doc.org): Org-mode support for Julia also seem discontinued. This was also written before v1. It
may be worth playing with if I can get Julia and org to work. I'll update this post in the future
once I figure out how to get org-babel working with Julia.



[^1]: My full config can be found [here](https://github.com/SNTag/.dotfiles/tree/master/emacs-26.2). The folder 'Borg-Collective-Emacs' has each of my major modes separated into individual el files. And yes, the name Borg is a star trek reference. My emacs assimilates each of my el files to form the final product.
