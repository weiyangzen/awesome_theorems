# THM-M-1228 proof-phase recheck at `57d8d017`

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `57d8d01796f84ffc9de9adf1f5d0723555e7babb`

Base tree: `cdea5b3fad713816ee6c9ed6aae7a10f9009a18e`

## Verdict

`blocked`. No legal positive proof body can complete the frozen target. The
canonical declaration is not a closed, source-faithful CKN proposition; it has
type

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

and the three semantic predicates are unconstrained. A premise-free body
uniform over that interface would prove

```text
forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S
```

The tracked, placeholder-free `ProofBlocker.lean` selects a permitted
semantics with suitability true and parabolic-measure-zero false. At trust
level zero, Lean checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

This refutes only the arbitrary-semantics universal closure. It does not
refute the mathematical Caffarelli-Kohn-Nirenberg theorem and does not show
that every specialization is false. Conversely, choosing a favorable
semantics would prove only a substituted specialization until concrete
definitions of suitable weak solution, regular point, and one-dimensional
parabolic Hausdorff measure are fixed and transported to the source claim.
The weighted CKN inequality is a separate repository target and is not an
alternate reading of this Navier-Stokes partial-regularity target.

The frozen registry has planned fingerprints and no terminal bodies for
`M1228-S-CONCRETE`, `M1228-E-EPSILON`, `M1228-C-COVER`, and
`M1228-L-MEASURE`. `ObligationTree.root_compose` assumes the entire
per-solution analytic conclusion and supplies no root proof credit. The
predecessor anchor audit found no exact positive body in the repository,
pinned dependencies, or four immutable external trees. The root therefore
remains `H1/M4/R4`; all completion fields remain false and the item remains
`[ ]`.

The predecessor gates are also not acceptance-ready:

- `S56-M-1228-OBLIGATION_TREE` is only `[_]`, not master-accepted `[x]`.
- `check_statement.py` reports the changed-spatial-dimension mutation as
  killed without executing that mutation comparison.
- All fifteen node validation recipes point at the same conditional
  `ObligationTree.lean` harness; it contains none of the analytic bodies the
  recipes nominally cover.
- The intake discovery-protocol hash remains null.

These facts do not authorize this proof worker to rewrite predecessor-owned
semantics, registry, graphs, recipes, the task DAG, or the generated
checklist. They keep the proof dependency and exact-target gate fail-closed.
This dossier already contained 26 earlier proof-recheck packets at the base.
The rev-5.6 five-tick split threshold has therefore been exceeded even though
the authoritative DAG still records zero proof attempts. The integration lane
must reconcile the attempts and split the repair rather than schedule another
identical proof recheck.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink was treated as read-only. No `lake update`, `lake build`,
dependency clone/fetch, checkout, ref repair, network action, or `.lake`
mutation was performed.

Root-project Lake validation is unavailable because the canonical pinned
`flt-regular` checkout has `HEAD` equal to `ref: refs/heads/.invalid`. Its
manifest-pinned commit object is present, but this worker did not repair the
ref. The narrowest allowed fallback ran `lake env lean` from the pinned
mathlib package with an explicit read-only `LEAN_PATH`, excluded the unusable
package, copied only `Statement.lean` and `ProofBlocker.lean` below `/tmp`, and
set Lean's root to that temporary directory. Both trust-zero checks passed;
temporary output was removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_statement.py` | 1 | Root Lake could not resolve `.lake/packages/flt-regular` `HEAD`. This is not a statement-check pass. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts` |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut. |
| `(cd Formalizations/Lean && LAKE_NO_UPDATE=1 timeout 30 lake env lean --version)` | 1 | Root Lake printed the same `flt-regular` `HEAD` resolution error; no dependency action was taken. |
| Scoped `lake env lean --trust=0 -t0` recipe below | 0 | The exact interface statement and both negative declarations elaborated. Each negative declaration reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration occurs in the owned Lean files. |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'` | 0 | `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |

The successful scoped replay recipe was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-1228
LAKE_ROOT=$(readlink -f "$ROOT/Formalizations/Lean/.lake")
MATHLIB=$LAKE_ROOT/packages/mathlib
LIBS=$(find -L "$LAKE_ROOT/packages" \
  -path '*/.lake/build/lib/lean' -type d \
  ! -path '*/flt-regular/*' -print | sort | paste -sd: -)
LEAN=$(cd "$MATHLIB" && timeout --foreground --kill-after=5s 60s \
  lake env which lean)
TOOLCHAIN=$(dirname "$(dirname "$LEAN")")/lib/lean
TMP=$(mktemp -d /tmp/thm-m-1228-lake-env-recheck-57d8d017.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET/Statement.lean" "$TARGET/ProofBlocker.lean" "$TMP"/

(cd "$MATHLIB" && LEAN_NUM_THREADS=1 \
  LEAN_PATH="$LIBS:$TOOLCHAIN" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
    -o "$TMP/Statement.olean" "$TMP/Statement.lean") \
  >"$TMP/statement.out" 2>"$TMP/statement.err"

(cd "$MATHLIB" && LEAN_NUM_THREADS=1 \
  LEAN_PATH="$TMP:$LIBS:$TOOLCHAIN" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
    "$TMP/ProofBlocker.lean") \
  >"$TMP/blocker.out" 2>"$TMP/blocker.err"
```

Replay SHA-256 values:

- statement stdout: `e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
- countermodel stdout: `392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
- each stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- temporary `Statement.olean`: `9a3d95793e0a82db705fcdb47fa6c9789c9f092caee9e3abda78e6f85d704cc2`
- Lean executable: `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`

The temporary olean hash is run-local warm elaboration output, not a
deterministic release claim. The source and semantic stdout hashes are the
stable boundaries used by this blocker replay.

Input SHA-256 values:

- `Statement.lean`: `e5360836f4875e028eabdbf3e76c860aa1566a0f2f4eeb1487588c6ee55ddcc5`
- `ProofBlocker.lean`: `b7c0043752d40a41350080fe5210b65aca2594a2c8cdbae139c3ab058ffacca5`
- `obligation-registry.json`: `90e618e7ead41d98804da85b81e7d8e0d366a322b62da0680b9d82043c66892b`
- `typed-graphs.json`: `41e601f13842fd84bc9b7ffcfdeab5cbfa415806836ebe0908e7493dc5ad4330`
- `anchor-audit.json`: `8d18f2332859b387552de7370c72674407d61f7260eb4dd476856694f7a7ba32`
- `validation-specs.json`: `8bc384e7935c1728f703811336580989e3b59f78317c67e6cd9914d5145b318b`

## Retry Condition

Reopen and version the statement around fixed, source-faithful definitions of
suitable weak Navier-Stokes solutions, regular points, and one-dimensional
parabolic Hausdorff measure. Complete the source and mutation gates, freeze a
corrected registry with accurately scoped validation recipes, and split the
work into dependency-legal child nodes. Then implement placeholder-free local
bodies or immutably pin exact compatible bodies for all four root-cut
obligations with checked transports, composition, and terminal-body
provenance. Restore the already-pinned `flt-regular` checkout before root Lake
validation without fetching a moving dependency.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
