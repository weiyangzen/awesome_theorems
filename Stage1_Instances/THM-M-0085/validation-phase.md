# THM-M-0085 validation-phase evidence

Item: `S56-M-0085-VALIDATION`. Base revision:
`f36169f19d5994091ea3dc506080032ff3f5321b`.

The frozen exact statement, named proof, proof-body provenance, trust closure,
and placeholder hygiene pass narrow worker validation. `Validation.lean`
independently reimplements the proof without importing `Proof.lean`; both
declarations elaborate and report exactly `propext`, `Classical.choice`, and
`Quot.sound`, with no `sorryAx`.

This is deliberately not release evidence. It reused the canonical pinned
`.lake` artifacts, so no cold empty-cache offline hermetic replay occurred.
The independent implementation used the same checkout and writable dependency
cache, so it is not a distinct independently provisioned and signed verifier.
Master acceptance remains pending. Consequently release-grade validation and
theorem completion are not claimed.

## Commands and results

Validation ran on 2026-07-12. No Lake update/build, clone, fetch, or dependency
mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0085` | 0 | rank 140, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0085/check_statement.py` | 0 | exact fingerprint and four killed statement mutations passed |
| `python3 Stage1_Instances/THM-M-0085/check_anchor_audit.py` | 0 | exact candidate and installed mathlib revision passed |
| `python3 Stage1_Instances/THM-M-0085/check_obligation_tree.py` | 0 | five obligations and eleven typed edges passed |
| `python3 Stage1_Instances/THM-M-0085/check_proof.py` | 0 | exact placeholder-free proof source passed |
| `python3 Stage1_Instances/THM-M-0085/check_validation.py` | 0 | frozen hashes, provenance, hygiene, exact proof, and same-checkout independent proof probe passed |
| `git diff --check -- Stage1_Instances/THM-M-0085 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The first failed release gate is rev-5.6 section 10.6 cold empty-cache offline
reproduction. Section 10.7 distinct-runner verification and master acceptance
are also open.
