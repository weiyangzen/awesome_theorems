# THM-M-0545 anchor-audit validation

Item: `S56-M-0545-ANCHOR_AUDIT`  
Date: 2026-07-12  
Base revision: `621e4c254d9e0dc9b50a60e66930c9f43601b890`

## Decision

The exact local target is a proposition definition without a proof body. The
legacy `S1_M_105.lean` file supplies an abstract package whose decomposition is
premise data, so it receives no rev-5.6 proof credit. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` has exterior derivatives on
unbundled forms, harmonic functions, finite-dimensional orthogonal
decomposition, Riemannian manifolds, sheaf cohomology, and algebraic Kahler
differentials. The eleven probes in `AnchorAudit.lean` elaborate these APIs;
none proves the frozen analytic Hodge decomposition.

Two known external projects were audited at immutable commits without cloning,
fetching, or mutating `.lake`. `LeanMillenniumPrizeProblems` explicitly says its
Hodge decomposition and harmonic interpretation are not formalized and instead
parameterizes Hodge data. `DeRhamCohomology` contains adjacent form APIs, no
terminal Hodge theorem, and four `sorry` occurrences in its audited
`DifferentialForm.lean`. Their complete Git-tree responses and inspected source
files are content-hashed in `anchor-audit.json`.

The root remains `M4`: no exact, integration-eligible proof body was found.
This is a self-tested bounded candidate inventory pending master acceptance,
not a global nonexistence claim, proof, audit completion, or theorem completion.

## Commands and results

All commands ran in this worker clone. Lean used the existing pinned `.lake`
artifacts.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1..1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | rank 105, planned, L0/rework_required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0545/AnchorAudit.lean` | 0 | eleven pinned support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0545/Statement.lean` | 0 | exact target and checked expansion re-elaborated |
| `python3 Stage1_Instances/THM-M-0545/check_anchor_audit.py` | 0 | candidate ledger, probes, target boundary, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i --glob '*.lean' 'HodgeDecomposition\|hodge decomposition\|HarmonicForm\|HodgeLaplacian\|Dolbeault\|deRhamCohomology\|KahlerManifold\|KaehlerManifold' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match status for terminal-name search in pinned mathlib source |
| `curl ... LeanMillenniumPrizeProblems/git/trees/540da948...?recursive=1` | 0 | immutable non-truncated 71-entry tree, response SHA-256 `55efcc7d...906f` |
| `curl ... urkud/DeRhamCohomology/git/trees/a58bf456...?recursive=1` | 0 | immutable non-truncated 45-entry tree, response SHA-256 `82da20db...24a5` |
| `python3 -m json.tool Stage1_Instances/THM-M-0545/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0545 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Reopen condition

Reopen integration only for a concrete exact Lean 4 candidate with immutable
revision, pinned toolchain and dependencies, module and declaration, exact-type
transport, terminal proof-body provenance, license, trust/placeholder audit,
and a successful local check.
