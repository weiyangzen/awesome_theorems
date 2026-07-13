# THM-M-0594 proof recheck at base 796a8177

Item: `S56-M-0594-PROOF`

Verdict: **blocked**. State remains `[ ]`. This record is not a proof receipt,
and no `.stage1-worker-selftest.json` is issued.

## Exact failed gate

The frozen root has no `CompactSpace M` hypothesis. It requires one
finite-dimensional Euclidean map on every finite-dimensional, T2,
second-countable, boundaryless smooth real manifold, together with global
smoothness, a topological embedding, and an injective manifold derivative at
every point.

Pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` proves only:

- `SmoothBumpCovering.exists_immersion_euclidean` when the bump-cover index is
  finite;
- `exists_embedding_euclidean_of_compact` under `[CompactSpace M]`.

The same module explicitly lists the sigma-compact weak Whitney theorem as
TODO work requiring Sard and Hausdorff-dimension infrastructure. The already
cached `origin/master` commit
`4efb186f102ebfd2eea1545c151d6fbcfdff0e43` has the same boundary. A bounded
repository and cached-source search found no exact immutable terminal body.

The existing compact exhaustion, locally finite bump-covering, proper plus
injective topological lemma, compact specialization, and conditional root
constructor all elaborate. They do not construct the unrestricted witness.
Consequently `M0594-C-GLOBAL` and `M0594-L-TOPOLOGICAL` remain the immediate
root cut set, and the root remains `M3`.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranked targets passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | Rank 255, planned, theorem incomplete |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/Statement.lean` | 0 | Exact unrestricted target elaborated |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/ProofSupport.lean` | 0 | Three partial support bodies elaborated; axioms exactly `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/AnchorAudit.lean` | 0 | Compact specialization elaborated; printed upstream type includes `CompactSpace M` |
| Project-local temporary `Statement.olean` plus `LEAN_PATH` replay of `ObligationTree.lean`, both at trust 0 | 0 | Conditional composition elaborated; axioms exactly `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 edges passed; denominator `0ad656ed...d367443`; root remains open M3 |
| Prohibited-construct scan over owned `*.lean` files | 1, expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle escape, or `proof_wanted` match |
| `python3 -m json.tool Stage1_Instances/THM-M-0594/proof-recheck-2026-07-14-head-796a8177.json` | 0 | Structured blocker record parsed |
| Recorded source-hash verification | 0 | All eight owned-source and pinned-module digests matched |
| `git diff --no-index --check /dev/null FILE` for both fresh artifacts | expected raw 1, wrapper 0 | Both files are new and emitted no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent |

## Dependency-policy incident

An invalid first attempt at the isolated replay used an output location outside
the Lean project root. Before Lean rejected the input, Lake automatically
cloned `flt-regular` into the shared canonical `.lake` target at the exact
manifest pin `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. That command is excluded
from validation evidence. The checkout is clean at the recorded pin, but the
side effect violates the worker rule against dependency cloning, so this run
does not claim mutation-free evidence. No update, fetch, pull, or build command
was run, and the shared checkout was not altered or removed afterward.

## Retry condition

Resume only with a checked finite global injective immersion and proper
point-separating construction for the frozen noncompact target, or an exact,
immutable, license-compatible Lean 4 terminal proof integrated into the pinned
repository-local closure. Adding compactness, using an infinite-dimensional
embedding, or treating a supplied-witness constructor as a proof would
substitute the theorem.

Status boundary: this is actionable blocker evidence only. It makes no proof
phase acceptance, audit completion, theorem completion, validation, release,
receipt acceptance, or master acceptance claim.
