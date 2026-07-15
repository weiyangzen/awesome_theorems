# THM-M-0594 proof recheck at 229ca98e (slot60)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-15T14:27:15+08:00

Base revision: `229ca98e7478d389ccf8de8173c94e0e7c8fe670`

Base tree: `d3cc9562940b923aebbe7e01ce66232079760b3b`

## Verdict

`blocked`. The exact unrestricted `WhitneyEmbeddingTarget` still has no
placeholder-free proof body in the pinned repository-local dependency closure.
This attempt does not add compactness, weaken the conclusion, or count a
conditional constructor as a root proof. The proof item remains `[ ]`, the
lifecycle remains `planned`, and the root remains `[H1, M3, R3]`. No receipt
acceptance, validation, release, audit completion, theorem completion, or
master acceptance is claimed. Because the assigned positive proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.

The frozen target covers every finite-dimensional, Hausdorff,
second-countable, boundaryless smooth real manifold. It asks for one map into
some finite-dimensional Euclidean space that is globally smooth, is a
topological embedding, and has injective manifold derivative everywhere. It
has neither a `CompactSpace M` premise nor a fixed target-dimension bound.

## First Failed Gate

`M0594-C-GLOBAL` remains open: no local or pinned proof constructs one finite
Euclidean tuple with injective derivative, global point separation, and
properness on an unrestricted noncompact manifold. The frozen immediate root
cut set remains:

```text
M0594-C-GLOBAL
M0594-L-TOPOLOGICAL
```

The checked bodies in `ProofSupport.lean` derive a compact exhaustion, a
locally finite smooth bump covering, and the proper-injective topological
endpoint. `ObligationTree.lean` checks root assembly from an already supplied
smooth embedding witness. None constructs the finite witness required by the
root.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
finite cover index. `SmoothBumpCovering.fintype` and the terminal
`exists_embedding_euclidean_of_compact` theorem require `CompactSpace M`.
The pinned module explicitly leaves the sigma-compact weak Whitney theorem as
a TODO requiring Sard and Hausdorff-dimension infrastructure. Current bounded
repository and installed-package searches found only the exact statement,
conditional/support declarations, compact specializations, and restricted
pinned endpoints.

## Smallest Real Validation

The existing pinned toolchain and already built package objects were reused.
No Lake update, Lake build, dependency clone/fetch, checkout, or `.lake`
mutation ran. Unlike an earlier transient cache failure, the literal required
`lake env lean` path succeeded at the current base, including trust-zero
replays of the exact statement and all checked support/compact-wrapper bodies.
This is narrow current-worker corroboration, not release evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/Statement.lean` | 0 | exact unrestricted target elaborated through the required pinned Lake environment |
| same trust-zero `lake env lean` replay on `ProofSupport.lean` | 0 | all three support bodies elaborated; axiom reports exactly `[propext, Classical.choice, Quot.sound]`; type probes expose the finite-index/compactness boundary |
| same trust-zero `lake env lean` replay on `AnchorAudit.lean` | 0 | compact-only wrapper elaborated; axiom report exactly `[propext, Classical.choice, Quot.sound]` |
| prohibited-construct scan of owned Lean files | 1 | expected no-match: no bodyless declaration, `sorry`, `admit`, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney-module endpoint/TODO scan | 0 | unrestricted theorem explicitly TODO; only finite-index immersion and compact-only embedding endpoints exist |
| bounded repository and installed-package declaration search | 0 | no unconditional inhabitant of `WhitneyEmbeddingTarget` was located |
| source and environment hash verification | 0 | all recorded hashes matched |
| `python3 -m json.tool Stage1_Instances/THM-M-0594/proof-recheck-2026-07-15-head-229ca98e-slot60.json >/dev/null` | 0 | structured blocker artifact parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0594 .stage1-worker-selftest.json` | 0 | no whitespace errors in owned changes |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest absent because the proof phase is blocked |

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
Exact source hashes and the structured command ledger are in the paired JSON.

## Retry Condition

Resume proof execution only after implementing the frozen noncompact weak
Whitney construction with checked child-to-parent composition, or after
placing an immutable, license-compatible proof of the exact unrestricted
target into the pinned repository-local dependency closure. A compact-only
theorem, infinite-dimensional topological embedding, or conditional witness
constructor is not a substitute.

Status boundary: this is fresh current-base nonrelease blocker evidence, not a
positive proof receipt. It does not satisfy `S56-M-0594-PROOF`, propose a
scheduler-state transition, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
