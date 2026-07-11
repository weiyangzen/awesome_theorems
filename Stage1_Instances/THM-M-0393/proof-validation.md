# THM-M-0393 proof-phase validation

## Implemented body

`Proof.lean` implements the finite-choice subclaim of frozen obligation `M0393-N1`. For every
positive degree `n` and nonzero integer `m`, the integers `g` for which `g^n` divides `m` form a
finite set. The proof bounds `|g^n|` by `|m|`, derives `|g| <= |m|`, and embeds all choices into a
finite integer interval.

This is a genuine local proof body, but it does not close all of `M0393-N1`: a later body must prove
that the gcd scale factor of a homogeneous-form solution satisfies the divisibility premise. It
does not assert `ThueStatement`, close any composition certificate, or change the root vector
`[H3, M4, R3]`.

## Commands and results

Commands ran from base revision `c6c14c0add140b98175266dc6421066ea99c79b3` on 2026-07-12
(validation timestamp `2026-07-11T19:36:08Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0393
  exit 0: execution rank 6; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0393/validate_obligation_tree.py
  exit 0: 17 obligations, 16 proof edges, and 6 workflow tasks; root M4/open

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0393/Proof.lean
  exit 0: finite_pow_divisors elaborated; #print axioms reported only propext,
  Classical.choice, and Quot.sound

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0393/Statement.lean
  exit 1: the pre-existing evalBinary definition triggers lean.dependsOnNoncomputable when Lean
  compiles executable output; this proof phase did not edit the frozen statement

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0393/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

python3 -m json.tool Stage1_Instances/THM-M-0393/proof-receipt.json >/dev/null
  exit 0

git diff --check -- Stage1_Instances/THM-M-0393 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No update, build, clone, fetch, or mutation of `.lake` was performed. The proof phase is a truthful
partial execution result pending master acceptance. The gcd-to-power-divisibility bridge, primitive
normalization, dehomogenization, algebraic-root and approximation packages, branch composition,
exact root, validation, release, H0, R0, and theorem completion remain open.
