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
- `check_statement.py`: pinned elaboration, fingerprint, import, and mutation validator.
- `statement.json`: structured canonical target and environment record.
- `statement-validation.md`: exact statement command ledger and boundary.
- `statement-receipt.json`: provisional statement-node receipt awaiting master acceptance.
- `check_statement_artifacts.py`: fail-closed metadata, receipt, and worker-packet validator.
