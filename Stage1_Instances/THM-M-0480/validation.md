# Intake validation

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb`; base tree:
`e46d642646f80980838b6f016f5d69b817bd464d`.

This validation covers manifest and execution-item identity, the planned dossier and six-node open
task DAG, exact repository-source provenance, the source-statement and non-substitution boundaries,
JSON and scoped invariants, a narrow pinned Lean declaration and axiom probe, prohibited-construct
hygiene, and whitespace. It does not validate a canonical source statement, a canonical Lean
target, a terminal PNT proof body, audit completion, or theorem completion.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The two structured self-test recipes are network-independent and
require denied-network replay. Exploratory source discovery did use the network to inspect a
Hadamard bibliographic/scan lead under `/tmp`; it did not fetch dependencies or mutate the
repository or `.lake`, and the untranscribed lead receives no source credit. This worker run does
not attest operating-system network isolation. The owned intake files and root worker packet make
the final tree dirty and nonrelease.

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
| `python3 scripts/stage1_target.py show THM-M-0480` | 0 | rank 1361; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 3525,3530 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '3525,3530p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog excerpt SHA-256 `5cd2aef6...92a1` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at `98dc76e3...` on `x86_64-unknown-linux-gnu` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| bounded exact-topic `rg` over repository-local and pinned-mathlib Lean | 0 | found prime-counting/asymptotic definitions, Chebyshev reductions and estimates, prerequisite and legacy audit records; no terminal PNT declaration; search output SHA-256 `a9297910...084`; discovery only |
| exploratory Hadamard source lookup | 0 | network was used only for bibliographic/scan discovery; a Numdam DJVU lead was stored under `/tmp`, but no proposition was transcribed or reviewed and no E4/H0 credit is assigned |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0480/IntakeProbe.lean)` | 0 | twelve definitions, asymptotic interfaces, reductions and estimates elaborated; all three representative theorem reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `e5559811...0e1` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0480-pycache python3 -m py_compile Stage1_Instances/THM-M-0480/check_intake.py` | 0 | scoped checker compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0480/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, base and source pins, planned H1/M3/R4 boundary, null canonical target, exact inventory, packet/receipt agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0480/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '(^\|[^[:alnum:]_])(sorry\|admit\|sorryAx)([^[:alnum:]_]\|$)\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0480` | 1 (expected no match) | no prohibited proof escape or declaration in the discovery-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0480 .stage1-worker-selftest.json` plus per-file no-index checks | 0 for the aggregate; no per-file diagnostics | no whitespace diagnostics in any new artifact |

## Evidence boundary

Pinned `Nat.primeCounting` has type `Nat -> Nat`; `Asymptotics.IsEquivalent` is a generic relation
over a filter; and the Chebyshev identity relates the cast of prime counting at `Nat.floor x` to
`theta x / log x` plus an integral remainder. These checked interfaces make a future exact target
and proof route expressible, but they do not choose the catalog's natural/real encoding or prove
the missing `theta(x) ~ x` input. The one-sided eventual upper bound is strictly weaker than PNT.

The bounded search result is intentionally modest. It establishes what this intake inspected, not
that no formalization exists anywhere. The legacy `S1_M_259` file is owned by another target and
explicitly supplies statement shapes and adjacent wrappers only. The external
`PrimeNumberTheoremAnd` mention in pinned mathlib is a discovery lead; no external source was
fetched, imported, or credited.

## Known open gates

An approved immutable primary or authoritative source, exact proposition and definition locators,
complete premise/conclusion/proof-boundary/attribution/translation/errata crosswalk, and independent
source review remain open. So do the definition and endpoint of prime counting, natural versus real
domain and filter, floor and casts, logarithm, asymptotic-equivalence semantics, ordered binders,
alternate transports, boundary decisions, the canonical Lean expression and environment
fingerprint, minimal imports, and statement mutations.

The scheduled exhaustive anchor and provenance audit, discovery protocol, obligation registry,
typed graphs, terminal proof-body and dependency audit, proof and composition acceptance, readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, master
acceptance, audit completion, and theorem completion also remain open. These failures do not
invalidate a truthful self-tested `planned` intake.
