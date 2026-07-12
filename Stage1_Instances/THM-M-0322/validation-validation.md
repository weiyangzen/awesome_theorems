# THM-M-0322 validation-phase evidence

Item: `S56-M-0322-VALIDATION`  
Base revision: `230f719da7724afb27c761dcb8c62a327557fe63`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The narrow worker gate passed. In a fresh temporary module directory, pinned Lean elaborated the
frozen statement, both directional proofs, frozen two-inclusion composition, exact proof root, and
a separately implemented direct reconstruction importing neither `Proof` nor `ObligationTree`.
Every proof-bearing declaration reported exactly `propext`, `Classical.choice`, and `Quot.sound`.
Source hygiene, receipt hashes, obligation denominator, clean pinned mathlib revision, and the
terminal mathlib source hash also passed.

This is intentionally nonrelease evidence. It reused the canonical shared warm `.lake` symlink;
there was no cold empty-cache offline restoration, complete transitive TCB/SBOM archive, distinct
runner, second attestation, or independently implemented release verifier. The frozen graph also
retains its pre-proof open reverse-inclusion and trust/provenance state pending master
reconciliation. Therefore no E0/E1, accepted M0, H0/R0, audit completion, theorem completion,
release, or master acceptance is claimed.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0322` | 0 | rank 819, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0322/check_validation.py` | 0 | kernel replay, exact axiom set, hashes, pin/source cleanliness, and differential reconstruction passed; release gates failed closed |
| `python3 Stage1_Instances/THM-M-0322/check_proof.py` | 0 | exact root proof surface, hygiene, input hashes, and proof receipt passed |
| `python3 Stage1_Instances/THM-M-0322/check_statement.py` | 0 | exact expression, mutations, boundaries, environment, and pins passed |
| `python3 Stage1_Instances/THM-M-0322/check_obligation_tree.py` | 0 | 19 obligations and 38 typed edges passed; pre-proof boundary retained |
| `python3 -m json.tool` on validation spec and receipt | 0 | both validation records are valid JSON |
| placeholder scan over four Lean modules | 1 | expected no-match result for `sorry`, `admit`, `sorryAx`, added `axiom`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0322 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The validation node is self-tested pending master acceptance. The first failed release-grade gate
is `hermetic.cold_empty_cache`; independent distinct-runner verification and complete trust/supply-
chain closure are also open. The release node must decide all remaining theorem-completion gates.
