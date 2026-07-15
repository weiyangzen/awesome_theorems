# THM-M-0162 proof-phase validation

Item: `S56-M-0162-PROOF`  
Base revision: `e46e0735d0940bb558acaf027d8386de2579f55d`

`Proof.lean` supplies proof bodies for the three exact equation-package
interfaces frozen in `ObligationTree.lean`, then closes
`Stage1Instances.THM_M_0162.FrenetSerretTarget` through the checked
`root_of_equation_packages` composer. The shared direct derivation first proves
the tangent equation by cancellation using positive curvature. It then obtains the
orthonormal frame from the Euclidean norm, principal-normal, and oriented
cross-product hypotheses. Derivatives of the constant dot products determine
the three coefficients of `N'` and `B'`; a checked coordinate proof of the
cross-product product rule and an orthonormal reconstruction lemma assemble the
normal and binormal equations.

The delivered declarations contain no `sorry`, `admit`, axiom declaration,
unsafe declaration, `implemented_by`, or oracle boundary. Trust-zero elaboration
reports exactly `[propext, Classical.choice, Quot.sound]` for
`tangentEquation`, `normalEquation`, `binormalEquation`, and `frenetSerret`;
in particular, there is no `sorryAx`. The proof source SHA-256 is
`968d9933bf08d4b315d54ef9bdf8215a5fd4b41b51f168541f2135d1213d09b9`.

## Exact commands and results

Commands ran in this worker clone on 2026-07-15. The Lean replay ran from
`Stage1_Instances/THM-M-0162`, used only the existing Lake-derived dependency
path and pinned Lean 4.29.0 toolchain, compiled `Statement.lean` into a fresh
mirrored module directory, compiled `ObligationTree.lean` against that frozen
statement, and removed the directory. It did not run `lake update`,
`lake build`, clone, fetch, or mutate a dependency.

```text
BASE_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)"
TMP="$(mktemp -d /tmp/thm-m-0162-proof-final.XXXXXX)"
mkdir -p "$TMP/Stage1_Instances/THM-M-0162"
LEAN_PATH="$BASE_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  LEAN_NUM_THREADS=2 timeout 300 lake env lean --trust=0 \
  -o "$TMP/Stage1_Instances/THM-M-0162/Statement.olean" Statement.lean
LEAN_PATH="$TMP:$BASE_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  LEAN_NUM_THREADS=2 timeout 300 lake env lean --trust=0 \
  -o "$TMP/Stage1_Instances/THM-M-0162/ObligationTree.olean" ObligationTree.lean
LEAN_PATH="$TMP:$BASE_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  LEAN_NUM_THREADS=2 timeout 300 lake env lean --trust=0 Proof.lean
sha256sum "$TMP/Stage1_Instances/THM-M-0162/Statement.olean" \
  "$TMP/Stage1_Instances/THM-M-0162/ObligationTree.olean"
rm -rf "$TMP"
  statement exit 0
  obligation tree exit 0
  proof exit 0
  tangentEquation, normalEquation, binormalEquation, and frenetSerret each
    depend on axioms: [propext, Classical.choice, Quot.sound]
  temporary Statement.olean SHA-256:
    795779164f0bc40d7e902bec54f8ab974ae6585994b15c0fbf711fba4debdeeb
  temporary ObligationTree.olean SHA-256:
    9ada050dd9efd9443641ee54f35cce5c97fe7cfd5486c71f783c4ed4f6ddef07
  temporary directory removal exit 0

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, all L0/rework-required
python3 scripts/stage1_target.py show THM-M-0162
  exit 0: rank 661, planned, L0/rework-required, theorem incomplete
python3 Stage1_Instances/THM-M-0162/check_obligation_tree.py
  exit 0: 17 obligations and 49 typed edges passed; denominator
  28db67d8555342a82bfb4d209445a5c10be82fe50e7b8f2763bdebdb54ca23ff
rg -n -i --glob '*.lean' \
  '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-0162/Proof.lean \
  Stage1_Instances/THM-M-0162/ObligationTree.lean \
  Stage1_Instances/THM-M-0162/Statement.lean
  exit 1: expected no-match result; no prohibited proof boundary found
git diff --check -- Stage1_Instances/THM-M-0162 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

This is proof-phase evidence pending master acceptance. The exact
equation-package bodies and composed root implement the mathematical obligations
represented by the frozen graph, including the cross-product derivative and
frame decomposition, but the frozen
structured graph still records the pre-proof `M3/M4` states. Only the master may
reconcile those records and scheduler state. Validation, human-source `H0`,
readability `R0`, hermetic replay, independent verification, release, audit
completion, and theorem completion remain unclaimed downstream gates. The
accepted structured state remains `[H1, M3, R4]`; this packet proposes
`[H1, M0-L, R4]` only after downstream validation and dependency-ordered
master acceptance.
