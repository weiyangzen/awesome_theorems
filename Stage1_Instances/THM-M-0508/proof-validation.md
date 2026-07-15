# THM-M-0508 proof-phase validation

Item: `S56-M-0508-PROOF`

Base revision: `8714972d4cf7ae256a92b9e35032c9df1bf5745c`

Base tree: `080d14e14102a733c6992aa0644e3c65d755e91b`

## Implemented bodies

`Proof.lean` adds two exact, unconditional theorem bodies at the previously
prose-bound cross-module boundary:

- `vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount`
  proves both directions between the canonical target from `Statement.lean`
  and eventual positivity of the finite count from `ObligationTree.lean`;
- `vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount`
  exposes the exact canonical child-to-root composition.

The equivalence unpacks the common threshold and uses the already checked
`ObligationTree.representationCount_pos_iff` in each direction. It is not an
alias of the obligation-tree-local target: both modules are imported and Lean
checks the transport to the canonical declaration. The frozen
`M0508-T-ASSEMBLE` node already had a local conditional body, so this is an
additional canonical-module composition certificate rather than progress or
closure credit for a frozen obligation; zero frozen obligations are claimed closed by this proof
receipt.

## Boundary

Neither new theorem constructs
`ObligationTree.EventualPositiveRepresentationCount`. The frozen analytic cut
therefore remains `M0508-N-FOURIER`, `M0508-B-ARCS`, `M0508-L-MAJOR`,
`M0508-L-SINGULAR`, and `M0508-L-MINOR`. Closing it requires the ternary
Fourier identity, major/minor arc partition, major-arc asymptotic, positive
singular-series bound, minor-arc estimate, and eventual-positivity assembly.

The exact root remains `[H1, M4, R3]`; `root_kernel_closed=false`,
`audit_complete=false`, and `theorem_complete=false`. This partial proof
handoff is not theorem completion. The existing stronger Formal Conjectures
candidate still has a literal `sorry` body and remains forbidden evidence.

## Validation

All checks used the existing pinned dependency artifacts. Generated Lean
objects and logs were written below `/tmp` and removed. No `lake update`,
`lake build`, dependency clone/fetch, network request, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0508` | 0 | rank 882; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0508/check_statement.py` | 0 | elaborated-expression SHA-256 `54ddaa6f...c1ac5fb`; all four frozen statement mutations were killed |
| `python3 Stage1_Instances/THM-M-0508/check_obligation_tree.py` | 0 | 17 obligations and 86 typed edges passed; denominator `79ff122b...53bc2`; root open M4 |
| `python3 Stage1_Instances/THM-M-0508/check_anchor_audit.py` | 0 | bounded audit, ten pinned probes, rejected placeholder candidate, and immutable mathlib pin passed |
| `bash Stage1_Instances/THM-M-0508/check_proof.sh` | 0 | isolated `Statement`, `ObligationTree`, and `Proof` elaboration at `--trust=0 -t0` under direct pinned Lean and mathlib's `lake env lean`; proof outputs agreed; both exact bodies were sorry-free and used exactly `propext`, `Classical.choice`, and `Quot.sound`; receipt hashes and open-root boundary passed |
| `rg -n -i --glob '*.lean' '(VinogradovThreePrimesTarget\|EventualPositiveRepresentationCount\|ternaryGoldbach\|three.?primes\|sum.?of.?three.?primes\|weak.?Goldbach\|Vinogradov.*prime)' . Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | only this target and blocked neighboring scaffolding matched; no eligible terminal Vinogradov proof was found |
| `rg -n --pcre2 '\b(?:sorry\|admit)\b\|sorryAx\|^[[:space:]]*(?:axiom\|constant\|opaque\|unsafe\|extern)\b\|implemented_by\|native_decide' Stage1_Instances/THM-M-0508 --glob '*.lean'` | 1, expected | no prohibited proof device occurs |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`, tree `bdc39a31...e5c2b`; tracked package worktree clean |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0508-pycache python3 -m py_compile -q Stage1_Instances/THM-M-0508/check_proof.py` | 0 | checker syntax compiled outside the owned path |
| `git diff --check -- Stage1_Instances/THM-M-0508 .stage1-worker-selftest.json` plus no-index checks for new files | 0 | no whitespace errors |

`check_proof.sh` deterministically enumerates only existing compiled package
directories, compiles both imported local modules to temporary `.olean` files,
checks `Proof.lean` twice through the pinned toolchain, compares proof output,
and removes the temporary directory on exit.

## Reopen condition

Resume root closure after placeholder-free bodies for the frozen Fourier,
arc-partition, major-arc, singular-series, minor-arc, and eventual-positivity
packages enter the pinned closure, or after an immutable compatible Lean 4
proof is pinned, exact-type transported, and audited for terminal provenance
and transitive trust.
