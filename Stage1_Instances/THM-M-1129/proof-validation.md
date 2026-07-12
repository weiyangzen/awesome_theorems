# THM-M-1129 proof-phase validation

Item: `S56-M-1129-PROOF`. Base revision:
`331f3394ba689a537bffbf8764a780c63caecd72`.

## Implemented proof bodies

`Proof.lean` adds four genuine local bodies for the frozen construction and
boundary architecture: the disk term is zero at time zero; zero data produce
a zero disk term; its time derivative is zero; and hence the entire represented
expression is zero for zero Cauchy data. Lean checks these by reducing the
outer scalar factor and the zero integrand, then differentiating the resulting
constant function.

These results provide kernel evidence for proper sub-branches of
`M1129-C-KERNEL`, `M1129-S-BOUNDARY`, and the initial-data route. They do not
close any whole frozen obligation: the positive-time singular-weight,
differentiation, PDE, initial-limit, representation, and uniqueness bodies are
still absent. In particular, zero-data uniqueness is not inferred merely from
the represented expression being zero. The root remains `H2/M3/R3`, with
`M1129-T-REPRESENT` as the first open root cut.

## Commands and results

Validation ran on 2026-07-12. The existing canonical pinned `.lake` artifacts
were reused through the worker symlink. No update, build, dependency clone,
fetch, or mutation of `.lake` was performed.

```text
cd Stage1_Instances/THM-M-1129
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
rm -f Statement.olean
  exit 0: all four proof bodies elaborated; every `#print axioms` reported
  exactly `propext`, `Classical.choice`, and `Quot.sound`

python3 Stage1_Instances/THM-M-1129/check_proof.py
  exit 0: four required local declarations found; prohibited-device and
  false-root-claim checks passed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1129
  exit 0: rank 334, planned, theorem_complete=false

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-1129/Proof.lean
  exit 1 with empty output: no prohibited proof device

git diff --check -- Stage1_Instances/THM-M-1129 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

This is truthful partial proof execution, not proof-phase closure of the exact
theorem. Validation, release, H0, R0, hermetic replay, independent verification,
master acceptance, and theorem completion remain unclaimed.
