# S56-M-1028-PROOF worker evidence

Date: `2026-07-12`

Base revision: `ec1b4823580f459faef9a345ee17cf1cd8e86d82`

## Proof bodies admitted

`Proof.lean` adds five placeholder-free bodies at the frozen proof boundary:
reflexivity, symmetry, and transitivity of coordinatewise modification; merging
the two almost-everywhere path events; and exact conditional composition into
`Statement`. The last theorem explicitly consumes both
`ContinuousModificationPackage` and `NowhereDifferentiabilityPackage`; it is
not an unconditional Wiener path theorem.

The first unresolved root cut is `M1028-C-CONTINUOUS-MODIFICATION` together
with `M1028-T-NONDIFFERENTIABLE`. The pinned mathlib closure has process and
Kolmogorov-condition infrastructure, but no terminal Brownian continuous-
modification or almost-sure nowhere-differentiability theorem. Thus the root
truthfully remains `M2`, theorem completion is false, and later validation and
release phases remain open. This proof phase is self-tested only for the real
bodies admitted here; master acceptance must preserve that conditional scope.

## Commands and exact results

All commands ran from the worker clone. Existing pinned `.lake` artifacts were
reused; no update, build, clone, or fetch was run.

```text
$ python3 Stage1_Instances/THM-M-1028/check_proof.py
PASS THM-M-1028 proof source: 5 checked bodies; exact root remains conditional on 2 open packages
exit 0

$ python3 Stage1_Instances/THM-M-1028/check_obligation_tree.py
PASS THM-M-1028 obligation tree: 16 obligations, 35 typed edges
registry denominator sha256: 1da5ac544652c879cb66023728abe4db4292d296422b79c2348bdce03c660d58
root closure: open (M2); continuity and nowhere-differentiability packages remain M4
exit 0

$ cd Stage1_Instances/THM-M-1028
$ LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean
exit 0; printed the exact Statement declaration

$ LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o ObligationTree.olean ObligationTree.lean
exit 0; root_of_path_packages axioms: [propext, Classical.choice, Quot.sound]

$ LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean Proof.lean
exit 0; each of the five declarations has axioms [propext, Classical.choice, Quot.sound]

$ git diff --check -- Stage1_Instances/THM-M-1028 .stage1-worker-selftest.json
exit 0; no output
```

The temporary `Statement.olean` and `ObligationTree.olean` files were removed
after the scoped elaboration. Proof source SHA-256:
`bcd59287bd9d8e10d5795900f402b0533692502a686cec7977c6fe7076ac3e29`.
