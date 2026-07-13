# THM-M-0070 rev-5.6 statement dossier

This directory is the fail-closed `planned` intake dossier for `THM-M-0070`, the
Feit-Thompson odd order theorem. The catalog gloss `奇数阶群可解` is resolved by the
primary paper's opening theorem: all finite groups of odd order are solvable. The catalog's
`已验证` field remains untrusted metadata and supplies no source or proof credit.

The primary paper was inspected at its title page and page 775 theorem statement. That establishes
the historical statement and candidate source boundary, but a page-one inspection is not a complete
proof, assumptions, corrections, errata, or node crosswalk. The independent source review required
for H0 also remains open.

Pinned mathlib supplies the vocabulary `IsSolvable`, `isSolvable_def`, `derivedSeries`, `Odd`, and
`Nat.card`. `IntakeProbe.lean` checks those interfaces, elaborates the candidate proposition shape,
and checks the order-one boundary. A bounded exact-topic search found no Lean Feit-Thompson root;
the upstream machine-checked result described in the repository is Coq/MathComp, not part of this
Lean dependency closure.

`Statement.lean` now freezes the exact root as
`Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget`. Its two inclusion-minimal imports expose
solvability and finite-cardinality vocabulary. Three checked `Iff` transports cover the
`Fintype.card`, modulo-two, and explicit derived-series shapes. Four mutation classes and generic
order-one and commutative-group implications protect the source boundary. `check_statement.py`
re-elaborates, fingerprints, and import-deletion-tests the complete module.

The obligation-tree phase now freezes 61 semantic obligations before proof acceptance. Separate
typed proof, refinement, provenance, evidence, trust, documentation, and workflow graphs expose the
minimal-counterexample reduction, all Bender-Glauberman and Peterfalvi section packages, the final
MathComp capstone, and the still-missing Lean translation. Package nodes are explicitly marked for
recursive splitting before proof acceptance; `source-obligation-index.json` records 2,084 exact
source declaration commands and 229 body chunks of at most 80 substantive source lines beneath
them. Their split ceilings are not proof evidence.

`ObligationTree.lean` checks only the conditional route from a future exact translated body back to
the canonical target. The external Lean declaration is rejected because its body is a placeholder,
and the exact MathComp theorem is a different kernel object with no approved Lean bridge. The vector
remains `[H1, M3, R4]`, accepted proof state is empty, and H0, M0, R0, audit completion, theorem
completion, release, and master acceptance remain open.
