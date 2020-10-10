---
categories:
- CRISPR
- Research
- NGS
date: "2019-11-29T00:00:00Z"
date-string: November 29, 2019
author: "Shayonendra N. Tagore"
title: "My plan for a CRISPR-KO library and scRNA-seq"
---

**DISCLAIMER**
I assume that you have working knowledge of vectors (plasmids) used in molecular biology, and know what an RNA or sgRNA is.  Anything else is not important or will be explained.

My master's thesis will be published soon on the NUS scholar's bank.  While I'm proud of what I've managed to do, the wet lab side of the work almost broke me!  For instance, an image in the thesis showing a western blot of DLG5 Knock-Out (KO) took almost 3 months of work.  The problem was not, as one would think, that DLG5 is >300 kDa, but that the antibodies were fussy...  >two days incubation in primary antibodies was the solution.

The project itself is a relatively novel one; completion of a CRISPR-KO screen on a migration assay.  This has been attempted previously with Smolen et al., but was only attempted on 11,000 genes.  This project would attempt to do so with ~20,000 genes and to eventually examine complete molecular phenotypes associated with the KO.

There are several advantages that we had over the Smolen paper.  Since its publication, technology Next Generation Sequencing (NGS) and CRISPR-KO libraries have developed significantly.  The first problem I came across is that our project needed CRISPR-KOs to be detected in DROP-seq (a variant of scRNA-seq).  Those who have worked in CRISPR might see the problem already; DROP-seq and CRISPR-KOs rely on detection of different RNAs to work.  Any RNA detected in DROP-seq had to have a Poly-A tail.  The sgRNA in CRISPR-KOs, however, is expressed under a Pol III system, meaning no poly-A tail.

Several labs have come up with similar solutions to artificially add a barcode.  All of those solutions (CRISPR-seq, Perturb-seq, etc) rely on the expression of a unique barcode on the same vector as the sgRNA.  The sgRNA will continue to be produced under Pol III with the unique barcode expressed under Pol II, enabling detection.  In concept, this solves the scRNA-seq problem with CRISPR.  However, such methods tend to have a high rate of mislabelling, template-switching (during viral packaging), and relatively high noise.

A better solution is in CROP-seq.  The approach does without a barcode and turns the sgRNA itself into a barcode.  Since the original paper, modifications to the paper has enabled a high detection rate.

 ![**A.** Description of how CRISPR functions using Cas9 and an sgRNA.  **B.** Doench et al., released data on sgRNA over multiple passages. **C.** A Poisson distribution representing the number of expected integrants per cell depending on the infection efficiency.  (**Credits:** **B.** is adapted from Doench et al.,)]({{ site.baseurl }}/images/posts/technical.png)

-   Doench, J. G. (2018). Am I ready for CRISPR? A user's guide to
    genetic screens. Nature Reviews Genetics, 19(2),
    67–80. <http://dx.doi.org/10.1038/nrg.2017.97>

-   Hill, A. J., McFaline-Figueroa, Jos\\'e L., Starita, L. M.,
    Gasperini, M. J., Matreyek, K. A., Packer, J., Jackson, D., …
    (2018). On the design of CRISPR-based single-cell molecular
    screens. Nature Methods, (), . <http://dx.doi.org/10.1038/nmeth.4604>

