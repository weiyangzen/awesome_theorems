# THM-M-1450 intake validation

Base revision: `03bed3c211cb739ccd2629908210fda0f9adf6ca` (tree
`a48670276bfe2105ddbfb4057314b21056dae0cb`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set identity, dossier structure and scope invariants, source-record
provenance, a secondary source lead, pinned environment identity, a narrow Lean API probe, bounded
local searches, proof-escape hygiene, JSON integrity, and whitespace. The catalog record is not an
exact proposition, so elaborating a purported canonical Lean target would invent missing
mathematics. `IntakeProbe.lean` checks only adjacent substrate and introduces no theorem.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux `7.0.0-27-generic` x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1450` | 0 | rank 1127, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match this record |
| `git blame -L 10588,10593 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over manifest, blueprint, execution DAG, skill, guidelines, catalog, Stage0, toolchain, lockfile, inspected mathlib files, and Netlib page | 0 | pinned/repository input hashes recorded in `instance.json` and the provisional receipt; the Netlib digest is a dated mutable observation |
| `curl -L --fail --silent --show-error https://www.netlib.org/utk/people/JackDongarra/etemplates/node95.html -o /tmp/thm-m-1450-netlib-power.html && sha256sum /tmp/thm-m-1450-netlib-power.html` | 0 | retrieved 7,679-byte mutable secondary page; SHA-256 `541ab6f6f74f3ee1c28396d9b4828e3703c4220500fd7f2d44271122b0844070` |
| bounded inspection of the SIAM/Netlib power-method section | 0 | dominant-by-modulus, nonorthogonal-start, increasing-parallelism, and eigenvalue-ratio rate scope located; HTML digest `541ab6f6f74f3ee1c28396d9b4828e3703c4220500fd7f2d44271122b0844070`; secondary lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| bounded exact-topic `rg` searches for power iteration/method and dominant-eigenvalue iteration in pinned mathlib and repo-local Lean | 1 | expected no exact-topic match; adjacent eigenspace, power, matrix-action, and spectral APIs were inspected separately; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1450/IntakeProbe.lean)` | 0 | 12 adjacent pinned APIs elaborated; two representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; complete output SHA-256 `5e5919ea5fd5e8ff67632b94cd691044a9e04439ab9a22c8aa093cb9629152ee`; no target declaration |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1450-pycache python3 -m py_compile Stage1_Instances/THM-M-1450/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1450/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, planned H5/M4/R4 boundary, null target, pins, inventory, handoff, and six open tasks agree |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1450 -g '*.lean'` | 1 | expected no-match; no prohibited proof escape in the API-only probe |
| scoped `git diff --check` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog method label and goal do not select one exact truth-valued proposition or an
  approved primary source.
- The matrix/operator domain, scalar field, dimension, meaning of largest, spectral gap,
  multiplicity, starting-vector premise, recurrence, normalization, estimator, convergence and
  rate definitions, sign/phase convention, arithmetic model, and boundary cases remain open.
- The inspected SIAM/Netlib section is a mutable secondary scope lead, not a catalog-cited,
  independently accepted complete source/proof crosswalk.
- Pinned mathlib's eigenvector-power, matrix-action, and self-adjoint spectral interfaces are
  adjacent ingredients, not a power-method convergence theorem.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Source and formal anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle,
  independent release verification, master acceptance, audit completion, and theorem completion
  remain open.

These failures block ordinary theorem execution and completion. They do not invalidate a truthful,
self-tested `planned` intake whose deliverable is to preserve ambiguity, scope, crosswalk,
discovery evidence, and the open DAG. Only the integration lane may accept the provisional worker
receipt.
