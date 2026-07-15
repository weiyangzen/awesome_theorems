# THM-M-0594 proof recheck at 34729c0d (slot37)

Item: `S56-M-0594-PROOF`

Intent: `prove`

Recorded: 2026-07-15T13:15:44+08:00

Base revision: `34729c0dff13ac1d1a2781d9c1ea4bf7c6a35398`

Base tree: `dde7f823b850641fc7dade0380327b6ac013ac07`

## Verdict

`blocked`. The exact unrestricted `WhitneyEmbeddingTarget` has no
placeholder-free proof body in the pinned repository-local dependency closure.
This attempt does not add compactness, weaken the conclusion, or count the
conditional witness constructor as a root proof. The proof item remains `[ ]`,
the lifecycle remains `planned`, and the root remains `[H1, M3, R3]`. No
receipt acceptance, validation, release, audit completion, theorem completion,
or master acceptance is claimed. Because the positive proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.

The frozen target covers every finite-dimensional, Hausdorff,
second-countable, boundaryless smooth real manifold. It asks for a map into
some finite-dimensional Euclidean space that is globally smooth, is a
topological embedding, and has injective manifold derivative everywhere. It
has neither a `CompactSpace M` premise nor a fixed target-dimension bound.

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
locally finite smooth bump covering, and the proper-injective topological
endpoint. `ObligationTree.lean` checks root assembly from an already supplied
smooth embedding witness. None constructs the finite witness required by the
root.

Pinned mathlib's `SmoothBumpCovering.exists_immersion_euclidean` requires a
finite cover index. `SmoothBumpCovering.fintype` and the terminal
`exists_embedding_euclidean_of_compact` theorem require `CompactSpace M`.
The pinned module explicitly leaves the sigma-compact weak Whitney theorem as
a TODO requiring Sard and Hausdorff-dimension infrastructure. A bounded search
of repository-local Lean and installed pinned packages found only the exact
statement, conditional/support declarations, compact specializations, and
restricted pinned endpoints.

## Smallest real validation

All successful Lean checks used the existing Lean 4.29.0 binary and pinned
package objects at trust level zero. `lake env lean` was attempted first, but
Lake stopped before invoking Lean because the existing shared `flt-regular`
checkout could not resolve `HEAD`. The fallback invoked the same pinned Lean
binary with `LEAN_PATH` assembled from the existing package object directories.
No Lake update/build, dependency clone/fetch, checkout repair, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean --version` | 1 | Lake stopped before Lean: shared `flt-regular` could not resolve `HEAD`; no repair was attempted |
| pinned Lean `--trust=0 -t0` with explicit package-object `LEAN_PATH` on `Statement.lean` | 0 | exact unrestricted target elaborated |
| same trust-zero replay on `ProofSupport.lean` | 0 | all three support bodies elaborated; axiom reports exactly `[propext, Classical.choice, Quot.sound]`; type probes exposed the finite-index/compactness boundary |
| same trust-zero replay on `AnchorAudit.lean` | 0 | compact-only wrapper elaborated; its axiom report was exactly `[propext, Classical.choice, Quot.sound]` |
| isolated temporary-olean trust-zero replay of `Statement.lean` and `ObligationTree.lean` | 0 | exact target and conditional root composition elaborated; composition axioms exactly `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; denominator `0ad656ed...d367443`; root open M3 and both cut-set packages M4 |
| prohibited-construct scan of owned Lean files | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney-module endpoint/TODO scan | 0 | only finite-index immersion and compact-only embedding endpoints; unrestricted theorem explicitly TODO |
| bounded repository and installed-package declaration search | 0 | only the exact statement, compact wrappers, support references, and restricted pinned endpoints were located |

The explicit object-path fallback was:

```bash
ROOT=$PWD
LEAN_ROOT=$ROOT/Formalizations/Lean
LEAN=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
LEAN_PATH=$(find "$LEAN_ROOT/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | sort | paste -sd: -)
LEAN_PATH="$LEAN_ROOT/.lake/build/lib/lean:$LEAN_PATH"
LEAN_PATH="$LEAN_PATH" LEAN_NUM_THREADS=1 timeout 300 "$LEAN" \
  --trust=0 -t0 "$ROOT/Stage1_Instances/THM-M-0594/Statement.lean"
```

For `ObligationTree.lean`, `Statement.lean` and `ObligationTree.lean` were
copied into a temporary directory. The command above first emitted a temporary
`Statement.olean`; a second invocation placed that directory first on
`LEAN_PATH`. The temporary directory was removed, and no repository object was
created.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
Exact source hashes and the complete command ledger are in the paired JSON.

## Retry condition

Resume proof execution only after implementing the frozen noncompact weak
Whitney construction with checked child-to-parent composition, or after placing
an immutable, license-compatible proof of the exact unrestricted target into
the pinned repository-local dependency closure. A compact-only theorem,
infinite-dimensional topological embedding, conditional witness constructor,
or empty-manifold special case is not a substitute.
