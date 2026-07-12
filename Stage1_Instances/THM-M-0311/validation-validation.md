# THM-M-0311 validation-phase evidence

Item: `S56-M-0311-VALIDATION`  
Base revision: `3d8dd27e4ff1200a2d9c8daaa9cae8072eca6241`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The narrow worker gate passed. In a fresh temporary module directory, pinned Lean elaborated the
frozen statement, scalar branch proofs, frozen composition certificate, exact proof root, and a
separately implemented direct reconstruction that imports neither `Proof` nor `ObligationTree`.
Every proof-bearing declaration reported exactly `propext`, `Classical.choice`, and `Quot.sound`.
Source hygiene, receipt hashes, the obligation denominator, and the clean pinned mathlib revision
also passed.

This is intentionally nonrelease evidence. It reused the canonical shared warm `.lake` symlink;
there was no cold empty-cache offline restoration, complete transitive TCB/SBOM archive, distinct
runner, second attestation, or independently implemented release verifier. The frozen graph also
retains its pre-proof M3 branch state pending master reconciliation. Therefore no E0/E1, accepted
M0, H0/R0, audit completion, theorem completion, release, or master acceptance is claimed.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0311` | 0 | rank 813, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0311/check_validation.py` | 0 | kernel replay, exact axiom set, hashes, pin cleanliness, and differential reconstruction passed; release gates failed closed |
| `python3 Stage1_Instances/THM-M-0311/check_proof.py` | 0 | exact root proof surface, hygiene, input hashes, and proof receipt passed |
| `python3 Stage1_Instances/THM-M-0311/check_statement.py` | 0 | exact expression, mutations, boundaries, environment, and pins passed |
| `python3 Stage1_Instances/THM-M-0311/check_anchor_audit.py` | 0 | immutable candidate, exact wrapper, provenance, and hygiene passed |
| `python3 Stage1_Instances/THM-M-0311/check_obligation_tree.py` | 0 | 17 obligations and 33 typed edges passed; pre-proof M3 boundary retained |
| `python3 -m json.tool` on validation spec and receipt | 0 | both validation records are valid JSON |
| placeholder scan over four Lean modules | 1 | expected no-match result for `sorry`, `admit`, `sorryAx`, added `axiom`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0311 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The validation node is self-tested pending master acceptance. The first failed release-grade gate
is `hermetic.cold_empty_cache`; independent distinct-runner verification and complete trust/supply-
chain closure are also open. The release node must decide all remaining theorem-completion gates.
