# THM-M-0253 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item "interpolating
sequence theorem." The repository attributes it to Lennart Carleson in 1958 and supplies only the
gloss "interpolating sequences for Hardy spaces." Its `已验证` ("verified") label is untrusted
inventory metadata under rev-5.6; it is not a source review, an exact proposition, or proof
evidence.

The gloss identifies a classical theorem family but does not select one statement. It leaves open
the analytic domain, the Hardy exponent, scalar or vector values, the definition of interpolation,
the admissible data and norm, the sequence indexing and distinctness conditions, and whether the
conclusion is an interpolation property, a geometric characterization, a Carleson-measure
characterization, a quantitative estimate, or an equivalence among them. Choosing the familiar
unit-disc `H^infinity` characterization now would add proposition-changing mathematics.

Bibliographic metadata identifies Carleson's 1958 paper *An Interpolation Problem for Bounded
Analytic Functions*, DOI `10.2307/2372840`, as a strong primary-source lead matching the catalog's
author, year, and subject. The paper itself was not lawfully available through the inspected
metadata services, so no theorem text, definition chain, assumptions, page range, proof boundary,
or errata were inspected or credited. The lead supports provisional `H1`, not `H0`.

Pinned mathlib supplies a complex unit-disc type, analytic-function predicates, bounded-set APIs,
and a meromorphic canonical-factor API related to Blaschke constructions. `IntakeProbe.lean` authenticates only those
interfaces. A bounded lexical search found no Hardy-space or Carleson interpolating-sequence
declaration. These observations are intake discovery, not an exhaustive anchor audit.

The canonical mathematical and Lean statements remain null. The provisional vector is
`[H1, M4, R4]`: a plausible primary work is identified but exact source fidelity remains open; no
usable exact formal artifact is credited; and no source-faithful readable proof is available.
`instance.json` is the structured scope authority, while `task-dag.json` keeps all six downstream
phases open. No H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
