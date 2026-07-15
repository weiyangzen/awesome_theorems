# THM-M-1228 proof-phase recheck at `21798c9c`

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `21798c9c8a9ed9ea40e8df489d9c661b59026564`

Base tree: `9150bea4c07c5bc89526ce2540709f0e9e8fda24`

## Verdict

`blocked`. The proof dependency is only provisional: the authoritative DAG has
`S56-M-1228-OBLIGATION_TREE` at `[_]`, rather than master-accepted `[x]`.
Independently, no legal positive body can close the frozen target. Its type is

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

and all three predicates in `CKNSourceSemantics` are unconstrained. The tracked,
placeholder-free `ProofBlocker.lean` chooses a permitted semantics with
suitability true and the required measure-zero conclusion false. Fresh
trust-zero elaboration checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

with only `[propext, Classical.choice, Quot.sound]`. Therefore a positive proof
uniform in the frozen interface would contradict a kernel-checked countermodel.
This refutes only that arbitrary-semantics universal closure, not the
mathematical Caffarelli-Kohn-Nirenberg theorem. Selecting a favorable semantics,
adding the per-solution conclusion as a premise or structure field, or replacing
parabolic with Euclidean Hausdorff measure would substitute another theorem.

The predecessor registry contains no closed obligations. Its frozen root cut is
`M1228-S-CONCRETE`, `M1228-E-EPSILON`, `M1228-C-COVER`, and
`M1228-L-MEASURE`; the conditional `ObligationTree.root_compose` assumes the
entire per-solution analytic conclusion. The bounded anchor audit found no exact
terminal proof body in the repository, pinned mathlib closure, or four immutable
external trees. The root remains `H1/M4/R4`, every completion field remains
false, accepted receipts remain empty, and the assigned item remains `[ ]`.

The predecessor evidence also reports only three executed statement-mutation
comparisons while listing the spatial-dimension mutation as killed, uses the
same conditional harness for all fifteen node recipes, and leaves the intake
discovery-protocol hash null. A proof worker cannot repair those predecessor
artifacts or alter the DAG/checklist. There are already 27 proof recheck packets
at this base, well beyond the five-tick split threshold; the integration lane
must reconcile and split the repair instead of scheduling another identical
attempt.

## Validation

All commands ran inside this worker clone. The automation-provided `.lake`
symlink targets the canonical pinned artifact tree and was treated read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, ref repair,
network action, or `.lake` mutation was performed.

Required root-project `lake env` validation failed closed. The pinned
`flt-regular` checkout has `HEAD` equal to
`ref: refs/heads/.invalid`; its manifest-pinned commit object is present, but
this worker did not alter it. The smallest available fallback ran
`lake env lean` from the pinned mathlib package with a read-only `LEAN_PATH`
made from existing package build roots, excluded `flt-regular`, copied the two
owned inputs below `/tmp`, and removed all temporary output after the trust-zero
replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `timeout --kill-after=2s 15s python3 Stage1_Instances/THM-M-1228/check_statement.py` | 1 | `flt-regular: could not resolve 'HEAD' to a commit`; no statement-check pass is claimed. The checker removed its temporary source. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts` |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut. |
| `(cd Formalizations/Lean && LAKE_NO_UPDATE=1 timeout --kill-after=2s 15s lake env lean --version)` | 1 | `flt-regular: could not resolve 'HEAD' to a commit`; no dependency action was taken. The failure output SHA-256 is `d7f032a9f211587b2bce9c30b081f54c7b2a9be97cae680c0a88bea5028e8652`. |
| `(cd Formalizations/Lean/.lake/packages/mathlib && timeout --kill-after=2s 20s lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Scoped `lake env lean --trust=0 -t0` recipe below | 0 | The exact interface statement and both negative declarations elaborated; both declarations reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration occurs in the owned Lean files. |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'` | 0 | `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1228/proof-recheck-2026-07-15-head-21798c9c.json >/dev/null` | 0 | The current-base structured blocker is valid JSON. |
| Scoped blocker invariant check | 0 | Identity, base revision/tree, blocked verdict, `[ ]` state, unchanged H1/M4/R4 vector, false completion fields, empty receipts, cut set, and changed paths agree. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics in tracked owned-path differences. |
| `git diff --no-index --check /dev/null <new packet>` | 1 each | Expected content-difference exits with empty stderr for both new files, so neither has whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful fallback recipe was equivalent to:

```bash
set -u
ROOT=$PWD
LAKE_ROOT=$(readlink -f "$ROOT/Formalizations/Lean/.lake")
LIBS=$(find -L "$LAKE_ROOT/packages" \
  -path '*/.lake/build/lib/lean' -type d \
  ! -path '*/flt-regular/*' -print | sort | paste -sd: -)
TOOLCHAIN=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean
TMP=$(mktemp -d /tmp/thm-m-1228-proof-21798c9c.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp Stage1_Instances/THM-M-1228/Statement.lean \
  Stage1_Instances/THM-M-1228/ProofBlocker.lean "$TMP"/
(cd "$LAKE_ROOT/packages/mathlib" && \
  LEAN_PATH="$LIBS:$TOOLCHAIN" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  --root="$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean")
(cd "$LAKE_ROOT/packages/mathlib" && \
  LEAN_PATH="$TMP:$LIBS:$TOOLCHAIN" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  --root="$TMP" "$TMP/ProofBlocker.lean")
```

Replay SHA-256 values:

- statement stdout: `e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
- countermodel stdout: `392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
- each stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- temporary `Statement.olean`: `9a3d95793e0a82db705fcdb47fa6c9789c9f092caee9e3abda78e6f85d704cc2`
- Lean executable: `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`

Input SHA-256 values:

- `Statement.lean`: `e5360836f4875e028eabdbf3e76c860aa1566a0f2f4eeb1487588c6ee55ddcc5`
- `ProofBlocker.lean`: `b7c0043752d40a41350080fe5210b65aca2594a2c8cdbae139c3ab058ffacca5`
- `obligation-registry.json`: `90e618e7ead41d98804da85b81e7d8e0d366a322b62da0680b9d82043c66892b`
- `typed-graphs.json`: `41e601f13842fd84bc9b7ffcfdeab5cbfa415806836ebe0908e7493dc5ad4330`
- `anchor-audit.json`: `8d18f2332859b387552de7370c72674407d61f7260eb4dd476856694f7a7ba32`
- `validation-specs.json`: `8bc384e7935c1728f703811336580989e3b59f78317c67e6cd9914d5145b318b`

## Retry Condition

Master-accept or repair the proof dependency as appropriate. Reopen and version
the statement around fixed, source-faithful definitions of suitable weak
Navier-Stokes solutions, regular points, and one-dimensional parabolic
Hausdorff measure. Complete the source and mutation gates, freeze a corrected
registry with accurately scoped validation recipes, and split the work into
dependency-legal child nodes. Then implement placeholder-free local bodies or
immutably pin exact compatible bodies for all four root-cut obligations, with
checked transports, composition, and terminal-body provenance. Restore the
already-pinned `flt-regular` checkout before required root Lake validation,
without fetching a moving dependency.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
