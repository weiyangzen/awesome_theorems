# THM-M-0622 rev-5.6 intake

This directory is the self-tested `planned` intake dossier for `蒂策扩张定理` (Tietze
extension theorem). The repository catalog supplies the gloss `正规空间中闭集上连续函数的延拓`
("extension of continuous functions on closed subsets of normal spaces"), attributes it to
Heinrich Tietze in 1915, and labels it `已验证`. Under rev-5.6, the label is untrusted discovery
metadata and supplies no proof credit.

The received wording identifies the classical theorem family but omits the codomain, boundedness
and range-preservation clauses, separation convention, exact binders, and boundary cases. The
1915 primary article was located in a stable Göttingen scan. Its Satz 3 is a bounded real-valued
extension theorem for a closed subset of a Frechet metric space, not by itself an audited identity
with the later normal-space formulation. The intake therefore leaves the canonical statement and
Lean target null rather than silently selecting a modern strengthening.

Pinned mathlib has substantial exact-topic support in `Mathlib.Topology.TietzeExtension`, including
real-valued bounded, interval-preserving, and unbounded forms and the generic
`ContinuousMap.exists_restrict_eq` interface. `IntakeProbe.lean` re-elaborates these candidates and
their axiom reports. They are strong formal discovery leads, but no candidate is credited to this
target until the source statement and transports are accepted.

The provisional vector is `[H1, M3, R4]`: a primary proof source and plausible statement family are
known, and pinned proved interfaces exist, but exact source fidelity, the canonical expression,
proof-body provenance, and readable reconstruction remain downstream. No accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.
