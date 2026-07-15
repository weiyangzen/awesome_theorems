# THM-M-0594 proof recheck at dafb8b51 (slot38)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-15T12:58:40+08:00

Base revision: `dafb8b51c4561eee5fcf162a8d5ee49555584bdb`

Base tree: `cca569d6bbc491441652aae678232353fb385a74`

## Verdict

`blocked`. No placeholder-free proof body for the exact unrestricted
`WhitneyEmbeddingTarget` exists in the pinned dependency closure. This attempt
does not add compactness, weaken the conclusion, or count a conditional
constructor as a proof. The proof item remains `[ ]`, lifecycle remains
`planned`, and the root remains `[H1, M3, R3]`. No receipt acceptance,
validation, release, audit completion, or theorem completion is claimed.
Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The target covers every finite-dimensional, Hausdorff, second-countable,
boundaryless smooth real manifold and asks for a globally smooth topological
embedding into some finite-dimensional Euclidean space whose manifold
derivative is injective everywhere. It has no `CompactSpace` premise.

## First failed gate

`M0594-C-GLOBAL` remains open: no local or pinned proof constructs one finite
Euclidean tuple with injective derivative, global point separation, and
properness on an unrestricted noncompact manifold. The frozen immediate root
cut set remains:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

The checked bodies in `ProofSupport.lean` derive a compact exhaustion, a
locally finite smooth bump covering, and the abstract proper-injective
topological endpoint. `ObligationTree.lean` checks root assembly from an
already supplied smooth embedding witness. None constructs the finite witness
required by the root. The map-specific `M0594-L-TOPOLOGICAL` node remains M4
because its generic endpoint cannot compose before that map and its
point-separation and properness invariants exist.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
finite cover index. `SmoothBumpCovering.fintype` and
`exists_embedding_euclidean_of_compact` require `CompactSpace M`. A fresh
exact-context trust-zero probe fails because Lean cannot synthesize that
instance. The pinned Whitney module explicitly leaves the sigma-compact weak
theorem as a TODO requiring Sard and Hausdorff-dimension infrastructure. A
scoped search found only the exact statement, conditional/support
declarations, compact specializations, and restricted pinned endpoints.
Read-only inspection of cached mathlib `origin/master` found the same TODO and
restricted endpoints; that ref is not a pinned dependency and receives no
proof credit.

## Smallest real validation

The pinned Lean executable and already built package objects were used at
trust level zero with an explicit read-only `LEAN_PATH`. No Lake update, Lake
build, dependency clone/fetch, or intentional `.lake` mutation was run. The
required `lake env lean` command was attempted first but failed before Lean
launch because the automation-shared, unrelated `flt-regular` checkout has an
invalid `HEAD` (`refs/heads/.invalid`). That failed attempt is environment
blocker evidence, not kernel evidence. The subsequent direct pinned-executable
checks bypassed dependency resolution without changing the pinned closure.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/Statement.lean` | 1 | Lake stopped before Lean: shared `flt-regular` checkout could not resolve `HEAD`; no fetch or repair was attempted |
| pinned Lean `--trust=0 -t0` with explicit package-object `LEAN_PATH` on `Statement.lean` | 0 | exact unrestricted target elaborated |
| same trust-zero replay on `ProofSupport.lean` | 0 | all three support bodies elaborated; axiom reports exactly `[propext, Classical.choice, Quot.sound]`; finite-index/compactness boundary printed |
| same trust-zero replay on `AnchorAudit.lean` | 0 | compact wrapper elaborated; axiom report exactly `[propext, Classical.choice, Quot.sound]`; upstream type requires `CompactSpace M` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ObligationTree.lean` | 0 | exact target and conditional root composition elaborated; composition axioms exactly `[propext, Classical.choice, Quot.sound]` |
| exact-context trust-zero probe through `exists_embedding_euclidean_of_compact` | 1 | expected proof-search failure: Lean could not synthesize `CompactSpace M` |
| prohibited-construct scans of owned Lean files and pinned Whitney source | 1 / 1 | expected no-match: no bodyless declaration, `sorry`, `admit`, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney endpoint/TODO scan and scoped declaration search | 0 / 0 | unrestricted theorem explicitly TODO; only finite-index/compact endpoints and local conditional/support declarations found |
| read-only cached `origin/master` inspection | 0 | cached commit `4efb186f...` retains the same TODO and restricted endpoints |
| source and environment hash verification | 0 | all recorded hashes matched |
| `python3 -m json.tool Stage1_Instances/THM-M-0594/proof-recheck-2026-07-15-head-dafb8b51-slot38.json >/dev/null` | 0 | structured blocker artifact parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0594` | 0 | no whitespace errors in the owned changes |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest absent because the proof phase is blocked |

The isolated composition recipe created its object only below a removed
temporary directory. The exact-context failure probe was also temporary.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
Exact source hashes and the structured command ledger are in the paired JSON.

## Retry condition

Resume proof execution only after implementing the frozen noncompact weak
Whitney construction with checked child-to-parent composition, or after
placing an immutable, license-compatible proof of the exact unrestricted
target into the pinned repository-local dependency closure. A compact-only
theorem, infinite-dimensional topological embedding, conditional witness
constructor, or placeholder-bearing candidate is not a substitute.

Status boundary: this is fresh current-base nonrelease blocker evidence, not a
positive proof receipt. It does not satisfy `S56-M-0594-PROOF`, propose a
scheduler-state transition, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
