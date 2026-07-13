# THM-M-0291 rev-5.6 intake

`THM-M-0291` is the real-analysis catalog item "Fejer's theorem." The repository attributes it to
Lipot Fejer in 1900 and gives the gloss "the Cesaro means of a continuous function converge
uniformly." Direct primary-source inspection identifies this as the classical periodic Fourier
summability family, but intake does not yet promote one binder-complete modern formulation.

## Intake result

Fejer's *Untersuchungen uber Fouriersche Reihen*, *Mathematische Annalen* 58 (1903), pages 51-69,
DOI `10.1007/BF01447779`, supplies an exact uniform-convergence lead. Page 51 assumes an
everywhere-continuous real `2*pi`-periodic function. Page 52 defines the symmetric Fourier partial
sums and the arithmetic means `s_0, (s_0+s_1)/2, ..., (s_0+...+s_(n-1))/n`, then states that this
sequence converges uniformly to the function. Page 60 repeats the everywhere-continuous uniform
conclusion after the more general Hauptsatz.

The exact root remains open because the catalog does not cite that article and no independent
source review has yet accepted its definition chain, proof boundary, translation, corrections, or
errata. The statement phase must also decide whether to preserve the source-literal real,
fixed-`2*pi`, `n`-term form or approve checked transports to a complex-valued arbitrary-positive-
period form and `n+1` indexing. Those choices are mathematically standard, but they are not
definitionally free.

`IntakeProbe.lean` checks the relevant pinned additive-circle and Fourier interfaces plus two
strictly different convergence theorems. It is discovery-only evidence. The provisional vector is
`[H1, M4, R4]`; all six downstream tasks remain open. There is no accepted statement or proof
state, audit completion, theorem completion, or master acceptance.
