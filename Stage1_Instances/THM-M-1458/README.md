# THM-M-1458 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `快速傅里叶变换`
(fast Fourier transform). The repository supplies only the gloss `DFT的快速算法` ("a fast
algorithm for the DFT"), attributes it to James Cooley and John Tukey in 1965, and labels it
`已验证`. A method name and purpose do not form a truth-valued proposition with ordered binders,
hypotheses, and a conclusion. The verified label is untrusted metadata and supplies neither source
nor proof credit.

A fast-DFT theorem could mean the algebraic Cooley-Tukey factorization for `N = N1 * N2`,
correctness of a radix-2 recursive program, a mixed-radix algorithm, an in-place bit-reversal
implementation, or an asymptotic operation-count result. These alternatives require different DFT
sign and normalization conventions, input and output types, admissible lengths, factor orders,
index permutations, arithmetic models, program semantics, and cost measures. The catalog selects
none of them. Choosing the familiar radix-2 `O(N log N)` result would invent proposition-changing
mathematics.

The bibliographic identity of Cooley and Tukey's 1965 paper is confirmed through the DOI metadata:
*An Algorithm for the Machine Calculation of Complex Fourier Series*, *Mathematics of
Computation* 19(90), pages 297-301, DOI `10.1090/S0025-5718-1965-0178586-1`. The catalog does not
cite the paper, its full text was not lawfully admitted into this worker dossier, and no exact
theorem passage, formula, premise, proof boundary, correction record, or independent source review
has been accepted. It is therefore a bibliographic source lead only, not `H0` evidence.

Pinned mathlib defines the mathematical DFT on `ZMod N` as a dense finite sum and proves inversion.
`IntakeProbe.lean` authenticates those definitions and selected finite-character infrastructure.
It does not define a fast algorithm, prove an algorithm equals `ZMod.dft`, or attach a cost bound.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received method gloss as not yet a
stable proposition; it does not refute standard FFT correctness or complexity theorems. All six
downstream phases remain open. No canonical statement, proof body, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
