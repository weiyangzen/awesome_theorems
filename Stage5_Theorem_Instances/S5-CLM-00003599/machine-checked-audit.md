# Machine-checked audit

The closure receipt is sealed against the semantic-environment digest and
declares `M0-P`-compatible trust conditions at the target boundary.  The
claim-owned Lean surfaces contain only theorem anchors and `import Mathlib`;
the numeric Formal Conjectures path and qualified declaration occur in
provenance comments exactly as frozen.  No placeholder, unsafe declaration,
claim-specific axiom, opaque oracle, or local parser/namespace substitution is
present.

The root census records the two provider-defined semantic constants used by
the frozen source definitions (`IsAdmissible` and `maxBoundaryLength`) with
provider, revision, source, type, and body digests.  Dependency edges are
acyclic and terminate at the root anchor.  Observed axioms are empty at the
claim-owned closure boundary.  Cold replay and semantic-substitution mutation
receipts are retained for canonical Master recomputation; this worker report
does not self-promote canonical acceptance.
