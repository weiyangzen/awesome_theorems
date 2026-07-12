# Proof-phase execution and blocker

Item: `S56-M-0645-PROOF`  
Theorem: `THM-M-0645`  
Execution date: 2026-07-12  
Base revision: `bdd92f30d924027320c18f282eed9ed56478eba5`

## Work completed

`Proof.lean` adds two real, placeholder-free proof bodies. `builder_of_countermodel` discharges
the frozen `M0645-T-CLASSICAL` transport: an exact countermodel property is converted by classical
contraposition into `CompletenessDerivationBuilder`. `completenessTarget_of_countermodel` composes
that result with the already checked exact-root wrapper.

These theorems deliberately retain `CountermodelProperty` as a premise. It is a definition of the
required output interface, not an axiom or claimed inhabitant. Thus this work does not pretend that
the premise, the builder, or `CompletenessTarget` has been closed.

## Blocking cut set

The pinned mathlib revision provides syntax and semantics but no syntactic completeness theorem.
The prior immutable-candidate audit found only an upstream Foundation theorem built with Lean
4.31.0 and a different language, proof calculus, equality convention, and dependency set. The
worker's pinned environment is Lean 4.29.0/mathlib `8a178386`; the external project is not present
as a pinned build artifact, and worker policy forbids fetching or mutating `.lake`.

Consequently no truthful proof body is locally available for the root-critical cut set
`M0645-R-NEG-CONSISTENT`, `M0645-C-HENKIN`, `M0645-C-TERM-MODEL`, `M0645-L-EQUALITY`,
`M0645-L-TRUTH`, and `M0645-R-COUNTERMODEL`. Implementing those results for the custom calculus is
a full first-order completeness development, not a bridge that can be replaced by an assumption.
The first failed proof gate is therefore `M0645-R-COUNTERMODEL`: there is no inhabitant of
`CountermodelProperty`, hence no inhabitant of `CompletenessDerivationBuilder` and no closed proof
of the exact root.

## Validation

The following commands were run from the worker clone. The Lean recipe copied the three local
modules into a temporary directory under `Formalizations/Lean`, reused the existing pinned
automation `.lake` link, and removed the temporary directory. It performed no update, build,
clone, fetch, or network operation.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and the uniform rework baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | rank 691, planned lifecycle, theorem incomplete |
| `cd Formalizations/Lean; tmp=$(mktemp -d -p . stage1-m0645-proof-XXXXXX); cp ../../Stage1_Instances/THM-M-0645/{Statement,ObligationTree,Proof}.lean "$tmp"/; LEAN_PATH="$(lake env printenv LEAN_PATH):$(realpath "$tmp")" lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean"; LEAN_PATH="$(lake env printenv LEAN_PATH):$(realpath "$tmp")" lake env lean -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"; LEAN_PATH="$(lake env printenv LEAN_PATH):$(realpath "$tmp")" lake env lean "$tmp/Proof.lean"; rc=$?; rm -rf "$tmp"; exit $rc` | 0 | all three modules elaborated; both new theorems report `propext`, `Classical.choice`, and `Quot.sound` through the imported semantic definitions |
| `rg -n '\\b(sorry|admit|axiom)\\b' Stage1_Instances/THM-M-0645/{Statement,ObligationTree,Proof}.lean` | 1 | no forbidden declaration or placeholder token found |
| `git diff --check -- Stage1_Instances/THM-M-0645` | 0 | no whitespace errors |

## Status boundary

The assigned proof phase is **blocked**, not self-tested complete, so no
`.stage1-worker-selftest.json` is written. The new conditional proof bodies are kernel checked but
do not close the countermodel premise or exact theorem. Machine debt remains `M4`; theorem
completion, validation, release, and master acceptance are not claimed.
