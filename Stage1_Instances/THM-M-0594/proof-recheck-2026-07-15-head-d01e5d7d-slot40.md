# THM-M-0594 proof recheck at d01e5d7d (slot40)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-15T08:31:11+08:00

Base revision: `d01e5d7daab630d25a32f781a754be9af1b82761`

Base tree: `32894fb5c2ce690dc4959f6964ed4c745d26a1ec`

## Verdict

`blocked`. No placeholder-free proof body for the exact unrestricted
`WhitneyEmbeddingTarget` exists in the pinned dependency closure. This attempt
does not add compactness, weaken the conclusion, or count a conditional
constructor as a proof. The proof item remains `[ ]`, lifecycle remains
`planned`, and the root remains `[H1, M3, R3]`. No receipt acceptance,
validation, release, audit completion, or theorem completion is claimed.
Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The exact target covers every finite-dimensional, Hausdorff, second-countable,
boundaryless smooth real manifold. It asks for one map into some
finite-dimensional Euclidean space that is globally smooth, is a topological
embedding, and has injective manifold derivative everywhere. It has neither a
`CompactSpace` premise nor a fixed target-dimension bound.

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
required by the root. The frozen map-specific `M0594-L-TOPOLOGICAL` node also
remains M4 because its checked generic endpoint has not been reconciled with
map construction and child-to-parent composition.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
finite cover index. `SmoothBumpCovering.fintype` and the terminal
`exists_embedding_euclidean_of_compact` theorem require `CompactSpace M`.
The pinned Whitney module explicitly leaves the sigma-compact weak theorem as
a TODO requiring Sard and Hausdorff-dimension infrastructure. A scoped search
of repository-local Lean and installed pinned packages found only the exact
statement, conditional/support declarations, and compact specializations. A
read-only inspection of cached mathlib `origin/master` found the same TODO and
restricted endpoints; the cached branch is not a pinned dependency and
receives no proof credit.

## Smallest real validation

The existing pinned toolchain and Lake artifacts were used read-only. No Lake
update, build, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| prohibited-construct scan of owned Lean files | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney-module endpoint/TODO and prohibited-construct scans | 0 / 1 | only finite-index immersion and compact-only embedding endpoints; unrestricted theorem explicitly TODO; expected no prohibited-construct match |
| scoped repository and installed-package declaration search | 0 | only exact statement/support references, compact wrappers, and the restricted pinned endpoints were located |
| read-only cached `origin/master` inspection | 0 | cached commit `4efb186f...` retains the same TODO and restricted endpoints |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout --foreground 300 lake env lean --trust=0 -t0 /tmp/THM_M_0594_compact_attempt.lean` | 1 | expected proof-search failure: Lean could not synthesize `CompactSpace M` at the only pinned Whitney endpoint |
| source-hash verification | 0 | all nine recorded owned-source and pinned-module hashes matched |

The fresh direct proof attempt used a scratch source outside the repository and
left no repository object. Positive current-base re-elaboration of the existing
support modules was also started with the narrow `lake env lean` recipe, but
the shared host was under sustained load above 200 with exhausted swap and
hundreds of concurrent workers. Those positive runs did not complete before
this blocker record was written and were stopped without producing repository
objects. Consequently this report does not claim a fresh current-base positive
kernel receipt. The previously integrated trust-zero results for the five
existing checked declarations remain source-hash-identical and are listed only
as prior evidence, not as a substitute for proof closure.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
Exact source hashes and the complete successful command ledger are in the
paired JSON.

## Retry condition

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
