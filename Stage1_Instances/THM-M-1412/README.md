# THM-M-1412 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item "Anosov
diffeomorphism." The repository supplies only the Chinese title, attributes it to Dmitri Anosov
in 1967, and glosses it as "uniformly hyperbolic system." It supplies no primary citation,
definition, ordered binders, hypotheses, or proposition-level conclusion. The catalog label
`已验证` is explicitly untrusted metadata and gives no human-source or Lean proof credit.

An Anosov diffeomorphism is normally a class of smooth dynamical systems defined through global
uniform hyperbolicity. That label does not by itself choose a theorem. It could refer to the
definition and its invariant stable/unstable splitting, existence or nonexistence examples,
structural stability, expansivity, stable-manifold consequences, or another result. Selecting one
from background knowledge would broaden or substitute the received target. Several neighboring
catalog entries separately own hyperbolic dynamical systems, Axiom A systems, spectral
decomposition, and Markov partitions, so none may be used as a convenient replacement root.

This intake freezes that ambiguity, the admissible scope questions, and the source-to-statement
crosswalk. It does not freeze a canonical mathematical proposition or Lean target. The provisional
vector is `[H5, M4, R4]`: the received record is not yet a stable proposition, no usable exact
formal artifact has been located, and no proof reconstruction exists. All downstream tasks remain
open in `task-dag.json`.

The authoritative intake data are in `instance.json`; `scope-map.md` records the candidate boundary
and prohibited substitutions; `source-statement-crosswalk.md` maps every repository phrase;
`IntakeProbe.lean` checks only adjacent pinned manifold APIs; and `validation.md` records exact
intake checks. No source acceptance, statement closure, H0, M0, R0, audit completion, theorem
completion, or master acceptance is claimed.
