# THM-M-0627 rev-5.6 intake

This directory is the self-tested `planned` intake dossier for `道路连通性定理`, provisionally
translated as "path-connectedness theorem." The repository catalog supplies only the gloss
`道路连通空间的性质` ("properties of path-connected spaces"), attributes it collectively to
nineteenth-century mathematicians, and labels it `已验证`. It gives no proposition, citation,
definition convention, assumptions, conclusion, proof, or formal artifact. Rev-5.6 treats that
status label as untrusted discovery metadata.

The received wording names a theorem family rather than one truth-valued theorem. This intake
therefore leaves the canonical mathematical statement and Lean target null. It does not silently
select the definition of path-connectedness, preservation by continuous images or quotients,
path-connectedness implying connectedness, a path-component characterization, or a closure
property such as unions or products. Those claims have different binders and conclusions.

`IntakeProbe.lean` checks adjacent declarations in the pinned
`Mathlib.Topology.Connected.PathConnected` module. The probe confirms that several plausible but
non-equivalent formal surfaces exist; it does not identify or prove the catalog target.

The provisional root vector is `[H5, M4, R4]`. Here `H5` classifies the received catalog wording as
an unstable proposition; it does not say that standard path-connectedness results are false or
open. There is no accepted statement, proof state, source review, audit completion, theorem
completion, or master acceptance. The scope map and crosswalk preserve the retry boundary, and the
task DAG keeps every downstream phase open.
