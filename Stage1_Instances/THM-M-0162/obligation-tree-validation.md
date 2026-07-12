# THM-M-0162 obligation-tree validation

Item: `S56-M-0162-OBLIGATION_TREE`. Base revision: `b077d12b80578ad8e0f6d19a4ab2dadabdfe40c8`.

Validation ran on 2026-07-12 in the worker clone. It reused the existing pinned Lake artifacts and
did not update, fetch, clone, or mutate a dependency.

```text
python3 Stage1_Instances/THM-M-0162/build_obligation_artifacts.py
  exit 0
  28db67d8555342a82bfb4d209445a5c10be82fe50e7b8f2763bdebdb54ca23ff

python3 Stage1_Instances/THM-M-0162/check_obligation_tree.py
  exit 0
  PASS THM-M-0162 obligation tree: 17 obligations, 49 typed edges
  registry denominator sha256: 28db67d8555342a82bfb4d209445a5c10be82fe50e7b8f2763bdebdb54ca23ff
  root closure: open (M3); tangent, normal, and binormal equation packages remain M4

lake env lean Stage1_Instances/THM-M-0162/ObligationTree.lean
  exit 1
  error: no default toolchain configured

LEAN_PATH=<worker-root>:$(cd Formalizations/Lean && lake env printenv LEAN_PATH) \
  /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
  -o Stage1_Instances/THM-M-0162/Statement.olean \
  Stage1_Instances/THM-M-0162/Statement.lean
LEAN_PATH=<same> \
  /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
  Stage1_Instances/THM-M-0162/ObligationTree.lean
  combined exit 0
  'root_of_equation_packages' depends on axioms: [propext, Classical.choice, Quot.sound]
  temporary Statement.olean removed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0162
  exit 0: rank 661, planned, theorem_complete false
rg -n '\b(sorry|admit|axiom)\b' Stage1_Instances/THM-M-0162 --glob '*.lean'
  exit 1: no matches
python3 -m json.tool <each of obligation-registry.json, typed-graphs.json,
  validation-specs.json>
  exit 0 for all three
git diff --check -- Stage1_Instances/THM-M-0162
  exit 0; no output
```

The direct `lake env lean` failure is retained rather than hidden. Lake supplied the pinned
dependency `LEAN_PATH`, but this worker shell has no default Elan toolchain. The successful narrow
retry used the already-installed pinned Lean 4.29.0 binary and the same Lake-derived dependency
path; it did not change `.lake`.

The checked Lean declaration is a conditional composition from three open equation packages. Its
successful elaboration is not a proof of `FrenetSerretTarget`.
