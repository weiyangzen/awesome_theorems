# THM-M-0594 proof recheck at 443b8bbc (slot41)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-15T11:45:24+08:00

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

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
remains M4 because its generic endpoint cannot compose before the global map
and its point-separation and properness invariants exist.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
finite cover index. `SmoothBumpCovering.fintype` and the terminal
`exists_embedding_euclidean_of_compact` theorem require `CompactSpace M`.
The pinned Whitney module explicitly leaves the sigma-compact weak theorem as
a TODO requiring Sard and Hausdorff-dimension infrastructure. A scoped search
of repository-local Lean and installed pinned packages found only the exact
statement, conditional/support declarations, and compact specializations.
Read-only inspection of the already cached mathlib `origin/master` found the
same TODO and restricted endpoints; cached refs are not pinned dependencies
and receive no proof credit.

## Smallest real validation

The pinned mathlib build objects were replayed with the pinned Lean executable
and an explicit read-only `LEAN_PATH`. This avoids Lake dependency resolution
in a heavily concurrent worker environment. No Lake update, Lake build, or
intentional dependency fetch/mutation was run by this target validation. An
initial `lake env lean` attempt encountered the automation-shared dependency
cache while another worker process was populating a missing unrelated
`flt-regular` checkout, so it was discarded and is not kernel evidence here.
The successful replay below does not use that unrelated package.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| pinned Lean `--trust=0 -t0` with explicit package-object `LEAN_PATH` on `Statement.lean` | 0 | exact unrestricted target elaborated |
| same trust-zero replay on `ProofSupport.lean` | 0 | all three support bodies elaborated; axiom reports exactly `[propext, Classical.choice, Quot.sound]`; finite-index/compactness boundary printed |
| same trust-zero replay on `AnchorAudit.lean` | 0 | compact wrapper elaborated; axiom report exactly `[propext, Classical.choice, Quot.sound]`; upstream type requires `CompactSpace M` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ObligationTree.lean` | 0 | exact target and conditional root composition elaborated; composition axioms exactly `[propext, Classical.choice, Quot.sound]` |
| exact-context trust-zero stdin attempt through `exists_embedding_euclidean_of_compact` | 1 | expected proof-search failure: Lean could not synthesize `CompactSpace M` |
| prohibited-construct scan of owned Lean files | 1 | expected no-match: no bodyless declaration, `sorry`, `admit`, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney-module endpoint/TODO and prohibited-construct scans | 0 / 1 | only finite-index immersion and compact-only embedding endpoints; unrestricted theorem explicitly TODO; expected no prohibited-construct match |
| scoped repository and installed-package declaration search | 0 | only exact statement/support references, compact wrappers, and restricted pinned endpoints located |
| read-only cached `origin/master` inspection | 0 | cached commit `4efb186f...` retains the same TODO and restricted endpoints |
| source and environment hash verification | 0 | all recorded hashes matched |
| `python3 -m json.tool` on the paired JSON | 0 | structured blocker artifact parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0594` | 0 | no whitespace error in owned changes |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest absent because the proof phase is blocked |

The exact-context failure probe was supplied through standard input and left no
scratch source or object. The isolated composition recipe copied the two owned
sources into a temporary directory, generated only a temporary
`Statement.olean`, and removed the directory after the successful check.

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
