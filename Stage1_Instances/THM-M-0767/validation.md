# Intake validation

Base revision: `91055abb3f5bee7f79323bc9cbefa7f2a8145f1f`.

This validation covers target membership, dossier structure, JSON integrity, scoped intake
invariants, and a narrow pinned Lean API probe. It does not elaborate or prove a canonical target.
The shared canonical `.lake` artifacts were used read-only; no update, build, clone, fetch, or
dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0767` | exit 0; rank 777, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0767/IntakeProbe.lean)` | exit 0; six pinned Cantor/cardinal API types elaborated under Lean 4.29.0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0767 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures remain intentionally open: immutable primary-source inspection and
independent review, canonical statement elaboration and mutation tests, obligation/discovery
freezes, formal-anchor and proof-body audit, proof/composition evidence, hermetic replay, and
release acceptance. They prevent theorem completion but do not invalidate a truthful `planned`
intake.

## Statement validation (2026-07-12)

Base revision: `3159849a5319960dea505779c7c20894ea30487c`.

The exact set-subtype statement, its type-level and exponential transports, and empty/finite
boundary fixtures were elaborated with the existing pinned artifacts. No `.lake` mutation command
was run. `#print axioms` reports `propext`, `Classical.choice`, and `Quot.sound` for every transport.

| Command | Result |
|---|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0767/Statement.lean)` | exit 0; exact canonical/type targets printed; five checked transports elaborate; empty and `Fin 3` fixtures elaborate; axioms exactly `propext`, `Classical.choice`, `Quot.sound` |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/task-dag.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/statement-freeze.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0 |
| `python3 scripts/stage1_target.py check` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0767 .stage1-worker-selftest.json` | exit 0; no output |

The statement node is self-tested but not master-accepted. Primary-source acceptance, anchor and
terminal proof-body provenance, transitive trust closure, M0, audit completion, and theorem
completion remain explicitly downstream.

## Anchor-audit validation (2026-07-12)

Base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`.

The audit inspected the locally pinned mathlib checkout at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, including the terminal source bodies and file hashes.
It also searched the pinned `flt-regular` dependency and repo-local Lean sources. Bounded anonymous
remote discovery found no additional repository candidate; GitHub code search was unavailable
(HTTP 401) and grep.app rate-limited the queries (HTTP 429), which is recorded as a search
limitation rather than evidence of global absence. No dependency or `.lake` mutation was performed.

| Command | Result |
|---|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; exact pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n "cantor_surjective|cantor_injective|theorem cantor|mk_powerset" Formalizations/Lean/.lake/packages/mathlib/Mathlib` plus source inspection | exit 0; exact cardinal anchor, normalization bridge, diagonal declarations, and terminal bodies located |
| `sha256sum` on the two audited mathlib files and `lake-manifest.json` | exit 0; hashes recorded in `anchor-audit.json` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0767/AnchorAudit.lean)` | exit 0; exact canonical wrapper and diagonal boundary elaborate; the anchor, wrapper, and `mk_powerset` report `propext`, `Classical.choice`, and `Quot.sound`; `cantor_injective` reports `propext` and `Quot.sound`; `cantor_surjective` reports no axioms |
| `rg -n -i 'cantor(_surjective\|_injective)?\|mk_powerset\|power.?set' Formalizations/Lean/.lake/packages/flt-regular --glob '*.lean'` | exit 1; no candidate in the immutable pinned external dependency |
| repo-local scoped `rg` excluding mathlib and this owned path | exit 0; only an unrelated prose occurrence, no exact Lean candidate |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/anchor-audit.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0 |
| `python3 scripts/stage1_target.py check` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0767 .stage1-worker-selftest.json` | exit 0; no output |

This node is self-tested but pending master acceptance. The exact pinned candidate justifies moving
the provisional machine classification from `M4` to `M3`; it does not grant `M0-W`. Obligation and
provenance graph freeze, composition, full trust closure, primary-source review, independent
validation, `AUDIT-Z`, and `THEOREM-Z` remain open.

## Obligation-tree validation (2026-07-12)

Base revision: `9864b47f2fbf53d0b642c54f12039877d4635056`.

Registry version 1 contains 28 canonical obligations and freezes its eligibility projection at
`9bf54713d38d6a18baeea4e55c8d9ec54f2ac0f02b7024fabf2cda9bc69acd66`. The graph validator checked
all required node fields, the three ordered denominators, unique reciprocal edges, seven distinct
graph roles, combined proof/refinement acyclicity, and root reachability of all 25 required
mathematical obligations. Three trust/provenance overlays are informational. All 28 obligations
remain open and the root remains `M3`.

| Command | Result |
|---|---|
| `python3 Stage1_Instances/THM-M-0767/build_obligation_artifacts.py` | exit 0; deterministically wrote 28 obligations and 46 typed edges |
| `python3 Stage1_Instances/THM-M-0767/check_obligation_tree.py` | exit 0; `PASS THM-M-0767 obligation tree: 28 obligations, 46 typed edges`; denominator hash matched; root open M3 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0767/Statement.lean)` | exit 0; exact statement and five transports elaborated; boundary fixtures passed; reported axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/obligation-registry.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/typed-graphs.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0767/task-dag.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets and ranks passed |
| `git diff --check -- Stage1_Instances/THM-M-0767 .stage1-worker-selftest.json` | exit 0; no output |

The generated artifact hashes were
`3d939d035e788c7aacb79374fef42feeead72e36408b6a1b32c72067bedcd42a` for
`obligation-registry.json` and
`54b7e133984bd53a8e9d3916b34d49182279b1460d9068d93fe012d7477679cb` for
`typed-graphs.json`. The pre-existing untracked `.lake` link/artifact was used without mutation.
This architecture self-test accepts no proof body or composition certificate and makes no theorem-
completion claim; master acceptance remains required.
