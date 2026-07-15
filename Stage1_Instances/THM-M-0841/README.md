# THM-M-0841: Erdos-Stone theorem

This directory contains the rev-5.6 `planned` intake and the provisional, self-tested statement
artifact for `S56-M-0841-STATEMENT`. The repository catalog provides only the name, attribution,
year, and gloss "a fundamental theorem of extremal graph theory". The statement phase therefore
selects the uniquely named theorem in the attributed 1946 primary paper.

The canonical root is the page-1087 sparse form: for `0 < epsilon < 1`, `r >= 2`, and sufficiently
large `n`, every `n`-vertex graph below the printed strict edge threshold contains `r` disjoint
equal-sized groups, of some positive natural size at least the displayed iterated-log square root, with no
cross-group edges. `Statement.lean` represents the groups as a complete equipartite graph contained
in the complement and preserves the source's binder order and strict inequalities.

The exact target elaborates from two narrow pinned imports. A checked `iff` unfolds the local
iterated-log notation; four structural mutations and five boundary declarations freeze statement
identity. The page-1088 dense complement form, modern fixed-forbidden-graph density formula, and
minimum-degree strengthening remain uncredited because no checked transport to them is supplied.

Current boundary: `[H1, M3, R4]`. This is an exact-statement proposal, not an accepted state,
source-fidelity closure, proof, audit completion, or theorem completion. The five later tasks remain
open, and only the integration lane may accept the provisional intake and statement receipts.

## Anchor-audit result

The bounded immutable audit found no exact Lean 4 proof for the growing-part page-1087 target.
Pinned mathlib supplies complete-equipartite and Turan-density support interfaces only. A post-pin
mathlib theorem and an external project prove neighboring dense fixed-part variants, but neither
supplies the sparse complement polarity, growing iterated-log part size, or checked tolerance
transport. They receive no proof credit. The accepted root remains `[H1, M3, R4]`.

## Obligation-tree result

`obligation-registry.json` freezes 53 canonical obligations before proof-phase closure credit. Its
v2 append-only delta records the repaired root spine and preserves the proposed v1 denominator. The
architecture expands the 1946 proof through its intersection lemma and corollaries, two-part base,
admissible-tolerance induction, rich-vertex filtering, repeated block deletion, and limiting
contradiction. It explicitly retains the non-definitional sparse/dense complement bridge and the
same-part-size stability problem on the final smaller graph.

`typed-graphs.json` separates proof, refinement, provenance, evidence, trust, documentation, and
workflow relations. `ObligationTree.lean` checks only conditional composition from `DenseBase`,
`DenseStep`, and `SparseFromDense`; none of those mathematical premises is inhabited. Zero
obligations close, the root stays `[H1, M3, R4]`, and proof, validation, release, H0/R0, AUDIT-Z,
theorem completion, and dependency-ordered master acceptance remain open.

## Artifacts

- `instance.json`: planned intake authority and fail-closed target record.
- `scope-map.md`: included theorem family, unresolved choices, and exclusions.
- `source-statement-crosswalk.md`: repository-to-primary-source-to-Lean component map.
- `task-dag.json`: six open downstream tasks.
- `IntakeProbe.lean`: historical intake API probe.
- `check_intake.py`: historical nine-file snapshot validator, superseded for current content.
- `validation.md`: historical intake command ledger, not current statement evidence.
- `intake-receipt.json`: immutable provisional intake-snapshot receipt; its recorded current-state
  fields and owned-file hashes are superseded by this statement packet.
- `Statement.lean`: exact page-1087 target, checked unfolding, mutations, and boundary checks.
- `check_statement.py`: pinned elaboration, fingerprint, import, and mutation validator for the
  immutable statement snapshot.
- `statement.json`: structured canonical target and environment record.
- `statement-validation.md`: exact statement command ledger and boundary.
- `statement-receipt.json`: provisional statement-node receipt awaiting master acceptance.
- `check_statement_artifacts.py`: fail-closed validator for the immutable statement-phase packet;
  its owned-file snapshot predates the anchor/tree expansion.
- `AnchorAudit.lean` and `anchor-audit*.json`/`.md`: pinned support checks and immutable candidate
  inventory, with no exact-root proof candidate.
- `check_anchor_audit.py`: fail-closed validator for the immutable anchor-audit snapshot; its
  repository-base assertion predates this obligation-tree worker packet.
- `ObligationTree.lean`: exact conditional dense-family and root composition harness.
- `obligation-registry.json` and `typed-graphs.json`: frozen semantic denominator and seven typed
  graph families.
- `build_obligation_artifacts.py` and `check_obligation_tree.py`: deterministic generator and
  fail-closed structure/Lean validator.
- `validation-specs.json`, `obligation-tree.md`, `obligation-tree-validation.md`, and
  `obligation-tree-receipt.json`: structured recipes, readable projection, exact command record,
  and provisional worker receipt.
