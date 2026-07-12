# THM-M-1028 anchor-audit validation

Item: `S56-M-1028-ANCHOR_AUDIT`  
Base revision: `cb017427b2aed4af4881826839e21a102a224cbf`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386...a95`, the Gaussian-process modification
and increment lemmas and the Kolmogorov/AE-Kolmogorov infrastructure elaborate.
Their audited endpoints report only `propext`, `Classical.choice`, and
`Quot.sound`. The pinned `Kolmogorov.lean` module defines a process satisfying a
moment condition and a coordinatewise modification of one, but provides no
continuous-modification constructor. No pinned package source contains a
Brownian/Wiener root or a Brownian nowhere-differentiability theorem.

The external audit resolved `RemyDegenne/brownian-motion` to immutable revision
`bdf5ea0c...9e8e`. It constructs Brownian motion over `NNReal` and proves a
continuous modification, including `IsPreBrownianReal.continuous_mk`. The 25
project-local modules in that candidate module's transitive import closure have
no `sorry` or `axiom` token. This is source evidence, not a local kernel check;
unrelated modules in the work-in-progress project contain `sorry`. The candidate
uses Lean `4.31.0` and mathlib `fabf563...f`, outside this repository's pinned
closure, and it has no nowhere-differentiability declaration.

Therefore no audited candidate has the frozen root type. The root remains `M2`:
not kernel-closed. This completes only the assigned candidate audit and makes no
theorem-completion claim.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1028` | 0 | rank 221, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-1028/AnchorAudit.lean` from `Formalizations/Lean` | 0 | all eight exact-type probes elaborated; five axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound` |
| `git ls-remote https://github.com/RemyDegenne/brownian-motion.git refs/heads/master` | 0 | `bdf5ea0c34f9e6d75bce5f0609a968d6e9e99e8e` |
| `python3 Stage1_Instances/THM-M-1028/check_anchor_audit.py` | 0 | local pin and sources matched; immutable external declarations, pins, hashes, and 25-module import-closure gap scan matched; root remained `M2` |
| `python3 -m json.tool Stage1_Instances/THM-M-1028/anchor-audit.json` | 0 | structured ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1028 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No dependency was fetched, cloned, added, or built, and `.lake` was not mutated.
