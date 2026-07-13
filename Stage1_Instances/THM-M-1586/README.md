# THM-M-1586 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Hamming界`
(Hamming bound). The catalog gives Richard Hamming, the year 1950, and the gloss
`纠错码的球包装界` ("the sphere-packing bound for error-correcting codes"). Its `已验证` field
is untrusted inventory metadata, not an exact source statement or machine proof.

The gloss identifies the classical packing argument: Hamming balls around distinct codewords are
disjoint when their radius is at most half the minimum distance, so their total cardinality cannot
exceed the ambient word space. It does not, however, select a binary or q-ary formula, an arbitrary
or linear code, a minimum-distance or correction-radius parameterization, a finite inequality or
asymptotic corollary, or the conventions needed at empty and degenerate cases. Intake therefore
does not silently choose the familiar formula
`|C| * sum_{i=0}^{floor ((d-1)/2)} choose(n,i) * (q-1)^i <= q^n`.

Hamming's 1950 paper *Error Detecting and Error Correcting Codes* is a strong primary-source lead.
Crossref independently fixes its bibliographic identity as *Bell System Technical Journal* 29(2),
pages 147-160, DOI `10.1002/j.1538-7305.1950.tb00463.x`. A metadata service also exposes a scan
candidate, but that host was unreachable from this worker. No full primary text, pinpoint theorem
or equation, errata disposition, or independent source review was admitted, so this is discovery
evidence only and not `H0`.

Pinned mathlib contains Hamming distance, its triangle inequality, its ambient-cardinality bound,
and the finite `Hamming` metric type. `IntakeProbe.lean` authenticates those APIs. A bounded search
found no code object, minimum-distance extremal function, ball-cardinality formula, or Hamming-bound
declaration. These APIs are substrate, not a substitute theorem.

The provisional vector is `[H1, M4, R4]`: a classical proved family and a credible primary source
lead are known, but the source-to-catalog proposition is not accepted; no usable exact formal
artifact is credited; and no source-faithful proof reconstruction exists. `instance.json` is the
structured scope authority, while `task-dag.json` leaves every downstream phase open. No canonical
statement, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
