# THM-M-0290 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item "Carleson-Hunt
theorem." The repository attributes it to Lennart Carleson and Richard Hunt in 1968 and supplies
only the gloss "the Fourier series of an `L^p` function converges almost everywhere." Its
`已验证` ("verified") label is untrusted inventory metadata under rev-5.6; it is not a reviewed
source statement, a kernel check, or proof evidence.

The gloss identifies the classical periodic Carleson-Hunt family but is not binder-complete. It
does not fix the range of `p`, the circle or interval model and period, real or complex values,
Haar/Lebesgue and Fourier normalizations, actual functions versus `L^p` classes, the partial-sum
cutoff convention, or the representative whose pointwise value occurs in the conclusion. Freezing
the familiar formulation now would add proposition-changing mathematics not present in the
repository source.

A bibliographic lead identifies Richard A. Hunt's 1968 paper *On the convergence of Fourier
series* (MR238019) as the likely primary source. Only its metadata in an immutable external
formalization was inspected; no exact theorem passage, incorporated definitions, proof boundary,
or errata record was reviewed. The lead supports provisional `H1`, not `H0`.

The same external project contains a highly relevant Lean declaration, `carleson_hunt`, at commit
`80e151dff5ddce2426079ec6392616496a4ec927`. It is discovery input only: the project is not an
installed dependency, targets a newer Lean/mathlib pair, and was not built or kernel-audited here.
Pinned mathlib supplies AddCircle, normalized Haar measure, Fourier coefficients, characters,
`MemLp`, `Lp`, and `Tendsto`; `IntakeProbe.lean` authenticates only these interfaces. In particular,
`hasSum_fourier_series_L2` proves `L^2`-topology convergence and is not the requested almost-
everywhere theorem.

The canonical mathematical and Lean statements remain null. The provisional vector is
`[H1, M4, R4]`: a published primary-work lead is identified but the exact source mapping is open;
no usable source-approved formal artifact has been established for the unfrozen root; and no
source-faithful readable proof is available. `instance.json` is the structured scope authority,
and `task-dag.json` keeps all six
downstream phases open. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
