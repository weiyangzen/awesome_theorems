# THM-M-1105 proof blocker at `00f98378`

Item: `S56-M-1105-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `00f98378e8c1c63097871ae62aeed895d83b0cb4`

Base tree: `4f2396db6d6d1c2b9948f401079f136dd0ed8f16`

## Verdict

`blocked`. No placeholder-free proof body or eligible pinned theorem closes the exact target
`Stage1.THM_M_1105.WignerSemicircleLaw`. The frozen registry contains 22 obligations, of which 20
are machine-required. Every required obligation still has `terminal_proof_body_id: null`, the
closed set is empty, and the root remains `[H2, M3, R4]`.

The local theorem
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence` is a checked composition
interface, not the missing proof. Its `terminal` binder assumes almost-everywhere
`SampleWeakConvergence`, which is the target's open analytic conclusion after unfolding the local
definitions. Crediting it would therefore be the prohibited shortcut of assuming the terminal.

The graph-derived minimal root cut remains `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. The dependency route also
requires trace expansion, walk classification, independence cancellation, Catalan enumeration,
expected and almost-sure moment convergence, semicircle moments, polynomial extension, and final
weak-convergence composition. These are substantive formalization packages, not proof holes that
can be filled by a routine wrapper.

## Candidate boundary

A fresh source-wide search of the pinned mathlib finds only the unrelated geometric word
"semicircle" in Thales' theorem. Mathlib provides Hermitian spectrum, integration, independence,
and weak-convergence infrastructure but no random-matrix Wigner theorem. The frozen immutable
candidate audit remains applicable at the unchanged proof-relevant hashes: semicircle-catalan
supplies only finite combinatorics; HighDimProb supplies infrastructure; and
`FredRaj3/SemicircleLaw@724f9ad6` contains placeholders, proves no weak-convergence root, and has a
different ensemble and convergence mode. None earns proof credit.

No theorem was weakened or substituted, no axiom or placeholder was added, and no `.lake`
dependency was fetched, updated, built, or mutated.

## Validation

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | rank 545; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root open at M3 |
| `(cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean)` | 0 | exact canonical proposition elaborated; only expected unused-hypothesis linter warnings |
| `(cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/ObligationTree.lean)` | 0 | conditional terminal-to-root composition elaborated; only expected unused-hypothesis linter warnings |
| prohibited-construct scan over owned `*.lean` files | 1 | expected no-match exit; no placeholder, axiom, unsafe, external, opaque, or implemented body found |
| pinned-mathlib `wigner`/`semicircle` source scan | 0 | only Thales' geometric semicircle comment; no random-matrix theorem |
| `git diff --check -- Stage1_Instances/THM-M-1105` plus direct new-file audit | 0 | no whitespace errors in the owned change |
| `python3 -m json.tool Stage1_Instances/THM-M-1105/proof-blocker-2026-07-15-head-00f98378.json` | 0 | structured blocker record is valid JSON |

The checked environment is Lean `4.29.0` at commit `98dc76e3...16740`, Lake
`5.0.0-src+98dc76e`, and mathlib `8a178386...ea95` (tree `bdc39a31...1c2b`). Proof-relevant
SHA-256 values remain `b7e0e83c...fdf75b` for `Statement.lean`, `922a4b40...84c0` for
`ObligationTree.lean`, `f5561115...45cb` for the registry, and `d3ce5de6...2987` for the typed
graphs.

## Retry condition

Resume after placeholder-free implementations of the frozen trace-moment, combinatorial,
concentration, almost-sure, tightness, approximation, and weak-convergence packages, or after an
immutable exact-scope Lean 4 theorem becomes available for dependency-legal pinning and checked
transport.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1105-PROOF`, change scheduler state, or support theorem completion. Because the assigned
phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately
absent.
