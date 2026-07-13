# Intake validation

Base revision: `67d32ab26aba14b674ae8a1b919e6935812190c3`; base tree:
`8a1d264cf3331992fbbc3a4fffca285af0b88929`.

This validation covers manifest and execution-item identity, the planned dossier and six-node open
task DAG, repository-source provenance, the source-statement and non-substitution boundaries, JSON
and scoped invariants, a narrow pinned Lean declaration and axiom probe, prohibited-construct
hygiene, and whitespace. It does not validate a canonical source statement, a canonical Lean
target, any proof body, audit completion, or theorem completion.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The structured recipes specify a denied-network policy, but this
worker run does not claim operating-system network isolation; it records that none of its commands
accessed the network. The owned intake artifacts and root worker packet leave a dirty, nonrelease
worker tree.

The packet-aware checker mode binds this exact worker handoff. Packet-free replay permits the
integration lane to rerun structural checks after moving the authoritative intake cursor from
`[ ]` to `[_]`; mutable blueprint and execution-DAG inputs are compared with their recorded base
blobs where appropriate. The provisional receipt remains unsigned and non-content-addressed, and
master acceptance must recapture its own evidence.

## Commands and results

All commands ran on 2026-07-13 in Asia/Shanghai. Commands without an explicit working directory ran
at the repository root.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0477` | 0 | rank 1358; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 3504,3509 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '3504,3509p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog excerpt SHA-256 `cc4a2b8f...fb7a19` |
| `sed -n '13082,13107p' Docs/Stage0_Blueprint.md \| sha256sum` | 0 | exact generated projection SHA-256 `8012c45f...13f9e` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at `98dc76e3...`; Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and package status | 0 | pinned mathlib revision `8a178386...a95`, tree `bdc39a31...e1c2b`; package status clean |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0477/IntakeProbe.lean)` | 0 | eleven two-congruence, finite-family, bound/uniqueness, and ZMod interfaces elaborated; three reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `0e5ad70c...a872a`, stderr empty |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | 0 | both initial structured artifacts parsed as valid JSON |

Final receipt/packet JSON parsing, checker compilation and replay, the packet-aware and packet-free
invariant checks, prohibited-token scan, and scoped whitespace checks are recorded exactly in
`intake-receipt.json` after artifact finalization. The receipt's denied-network structured recipes
are replay specifications, explicitly marked as not executed with operating-system network
isolation; the raw command observations are recorded separately and receive only worker-level
credit.

## Known open gates

An independently accepted immutable primary or authoritative source, exact result and definition
locators, complete premise/conclusion/proof-boundary/translation/correction/errata mapping, and
historical-source review remain open. So does the choice between the historical Sunzi problem or
method and a later general theorem. Natural/integer/ZMod carrier choice, finite versus potentially
infinite system scope, two versus indexed-family scope, modulus sign and normalization,
compatibility versus coprimality, zero/unit/nonzero conventions, existence versus construction,
uniqueness/product/lcm/bounded-representative conclusions, ordered binders, boundary decisions, the
canonical Lean expression and environment fingerprint, checked alternate transports, and
statement mutations also remain open.

The scheduled exhaustive anchor and provenance audit, discovery protocol, obligation registry,
typed graphs, terminal proof-body and dependency audit, proof and composition acceptance, readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, master
acceptance, audit completion, and theorem completion also remain open. These failures do not
invalidate a truthful self-tested `planned` intake.
