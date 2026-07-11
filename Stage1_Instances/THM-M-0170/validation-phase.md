# S56-M-0170-VALIDATION worker evidence

Date: `2026-07-12`. Base revision: `168aae8f6c98f025672f9f8fcfedb2a74785e4b9`.

The validation phase replayed the frozen statement, conditional root composition, and proof-phase
empty-manifold leaf in the pinned Lean environment. A separately written `Validation.lean` probe,
which neither imports nor invokes `Proof.lean`, independently reconstructs the same boundary leaf.
All checked declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. The scoped
source scan found no proof placeholder, new axiom, unsafe declaration, or oracle boundary.

Provenance is bound to mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` and tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its worktree was clean. The obligation validator
reconfirmed 17 obligations and 41 typed edges. Crucially, it also reconfirmed that the exact root is
open at `M4`: `M0170-B-COMPACT` and `M0170-B-NONCOMPACT` are unproved premises. Validation does not
turn the conditional composition or empty boundary case into the Nash embedding theorem.

This is nonrelease evidence. The run reused the canonical warm `.lake` artifacts. The host rejected
`unshare --net`, so enforced network isolation was unavailable, though no command used the network.
The independent probe ran in the same checkout and cache, not on a distinct independently
provisioned verifier. Cold replay, TCB/axiom-policy acceptance, source `H0`, readable `R0`, audit
completion, theorem completion, and master acceptance all remain open.

## Commands and results

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0170` | 0 | rank 123; planned; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0170/Statement.lean` | 0 | exact statement and four guarded mutations elaborated; axioms were the accepted observed trio |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0170/ObligationTree.lean` | 0 | conditional compact/noncompact composition elaborated; it retains both premises |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0170/Proof.lean` | 0 | proof-phase empty-manifold boundary leaf elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0170/Validation.lean` | 0 | separately written same-workspace boundary probe elaborated without importing `Proof.lean` |
| `python3 Stage1_Instances/THM-M-0170/check_obligation_tree.py` | 0 | 17 obligations, 41 typed edges; root open at M4 |
| `python3 -m json.tool Stage1_Instances/THM-M-0170/validation-spec.json >/dev/null` | 0 | validation recipe is valid JSON |
| `rg -n '\\b(sorry\|admit\|sorryAx\|axiom\|unsafe)\\b\|placeholder\|theorem_complete[[:space:]]*:[[:space:]]*true' Stage1_Instances/THM-M-0170/{Statement.lean,ObligationTree.lean,Proof.lean,Validation.lean,proof-receipt.json,validation-spec.json}` | 1 | no prohibited token or false completion claim (`rg` exit 1 means no match) |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain` | 0 | no output; pinned mathlib worktree clean |
| `unshare --net true` | 1 | host denied network namespace; hermetic gate failed closed |

First failed gate: `root.kernel_closure`. Retry after both frozen Nash branch packages have genuine
kernel-checked proof bodies; only then can cold hermetic and distinct-runner verification be useful.
