# THM-M-1228 proof-phase recheck at `33a5b0d6`

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

## Verdict

`blocked`. The canonical declaration is not a closed proposition: it has type

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

and no concrete source-faithful semantics is selected. Its three fields are
unconstrained. Consequently, a premise-free theorem body accepting arbitrary
`S` would prove

```text
forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S
```

which the tracked, placeholder-free `ProofBlocker.lean` refutes. It chooses a
permitted semantics with suitability true and parabolic-measure-zero false,
and Lean checks both

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

at trust level zero. This refutes only the current under-specified interface,
not the mathematical Caffarelli-Kohn-Nirenberg theorem. Choosing a favorable
specialization, assuming the per-solution conclusion, importing the unrelated
weighted CKN inequality, or replacing parabolic by Euclidean Hausdorff measure
would substitute a different theorem and was not done.

The frozen registry has only planned fingerprints, rather than elaborated Lean
targets, for the four analytic cut obligations. Its conditional
`ObligationTree.root_compose` consumes the entire open per-solution analytic
conclusion and supplies no root proof credit. Repo history, installed pinned
dependencies, and the predecessor immutable external audit contain no exact
positive body. Pinned mathlib has support-only ambient Hausdorff and covering
APIs, but no suitable weak Navier-Stokes semantics, parabolic geometry,
epsilon-regularity theorem, bad-cylinder estimate, or terminal CKN theorem.

The predecessor registry remains open at `M4`; this worker does not rewrite
the statement, registry, typed graphs, task DAG, or generated checklist. The
frozen root cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

No positive proof body, receipt, accepted obligation, audit completion,
validation completion, release result, or theorem-completion claim is made.
The assigned item remains `[ ]`.

This is another unresolved proof tick beyond the standard's five-tick split
threshold. The integration lane should reopen the statement and registry, then
split the repair into dependency-legal child work rather than schedule another
identical proof recheck.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink was treated as read-only. No `lake update`, `lake build`,
dependency clone/fetch, checkout, ref repair, network action, or `.lake`
mutation was performed.

Lake-mediated validation is currently unavailable because the canonical
`flt-regular` checkout has `HEAD` equal to `ref: refs/heads/.invalid`. The
manifest-pinned commit object is present, but this worker did not repair the
ref. A narrower non-Lake fallback invoked the exact pinned Lean executable
with only already-present compiled package paths; it successfully replayed
the statement and countermodel and wrote temporary output only below `/tmp`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_statement.py` | 1 | Lake reported that `.lake/packages/flt-regular` could not resolve `HEAD` to a commit. This is not a statement-check pass. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts` |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut. |
| `(cd Formalizations/Lean && LAKE_NO_UPDATE=1 timeout 30 lake env lean --version)` | 1 | Lake printed the same `flt-regular` `HEAD` resolution error; no dependency action was taken. |
| Direct trust-zero fallback recipe below | 0 | The exact statement and both negative declarations elaborated. Each negative declaration reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration occurs in the owned Lean files. |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'` | 0 | `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |

The successful direct replay recipe was:

```bash
set -euo pipefail
root=$PWD
lean=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
lean_lib=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean
paths=("$root/Formalizations/Lean/.lake/build/lib/lean")
while IFS= read -r path; do paths+=("$root/$path"); done < <(
  find Formalizations/Lean/.lake/packages -type d \
    -path '*/.lake/build/lib/lean' -printf '%p\n' | sort
)
printf -v suffix ':%s' "${paths[@]}"
lean_path="$lean_lib$suffix"
tmp=$(mktemp -d /tmp/thm-m-1228-proof-33a5b0d6.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean" \
  --trust=0 -t0 -o "$tmp/Statement.olean" \
  Stage1_Instances/THM-M-1228/Statement.lean
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean" \
  --trust=0 -t0 Stage1_Instances/THM-M-1228/ProofBlocker.lean
```

Replay SHA-256 values:

- statement stdout: `e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
- countermodel stdout: `392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
- each stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- temporary `Statement.olean`: `9c3fe8b4c407d6881d5e69167f2948e8fd2364467a642116ed4eb11d4abced8c`
- Lean executable: `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`
- constructed `LEAN_PATH` string: `831a1ece59c893fca58d0982aff5a788e853c23b254c72945caef6aef884b5e0`

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
parabolic Hausdorff measure. Freeze a corrected registry, split the work into
child nodes, and implement placeholder-free local bodies or immutably pin
exact compatible bodies for all four root-cut obligations, with checked
transports, composition, and terminal-body provenance. Restore the already
pinned `flt-regular` checkout before Lake-mediated validation without fetching
a moving dependency.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
