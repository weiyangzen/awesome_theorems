# Intake validation

## Boundary

This record covers only `S56-M-0931-INTAKE`: target membership, the planned dossier, scope map,
source-statement crosswalk, six-node open task projection, and discovery-only Lean candidate probe.
It does not validate a canonical statement, checked source specialization, proof body, obligation
tree, trust closure, audit completion, theorem completion, or release.

The worker used the automation-provided `Formalizations/Lean/.lake` symlink as read-only pinned
input. No `lake update`, build, dependency fetch, clone, or `.lake` mutation was run.

## Inputs

- Repository base: `fb0baac89ea0633612be3b47448464b4b8e4bef7`
- Repository tree: `018557070da18ea1733a82de81a238750c59aa84`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- Mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Primary scan: 236365 bytes, SHA-256
  `bae3803dc3e04c41ba10f63c112ba48727dacd1f7c4b1388ec21ff3b084a42b9`
- Initial worktree state: only the pre-existing automation `.lake` symlink was untracked.

## Commands and results

All commands used repository root as `cwd` unless another directory is shown.

1. `python3 Docs/tools/check_stage1_standard.py`
   - Exit `0`.
   - `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)`
2. `python3 scripts/stage1_target.py check`
   - Exit `0`.
   - `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)`
3. `python3 scripts/stage1_target.py show THM-M-0931`
   - Exit `0`.
   - Rank 1470, planned, `L0 / rework_required`, no legacy slot, legacy artifacts unaccepted,
     theorem completion false.
4. `git status --short --untracked-files=all`
   - Exit `0`.
   - Before dossier creation: `?? Formalizations/Lean/.lake`; the symlink was preserved read-only.
5. `git rev-parse HEAD HEAD^{tree}`
   - Exit `0`.
   - Returned the repository base and tree recorded above.
6. `git blame -L 6805,6810 -- Docs/researches/math_theorems.md`
   - Exit `0`.
   - All six catalog lines originate in
     `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
7. `wget -O temporary-primary-scan https://www.renyi.hu/~p_erdos/1961-25.pdf`
   - Exit `0`; network allowed for source intake only.
   - HTTP content length 236365; observed PDF digest is recorded above. The temporary source was
     inspected outside the repository and was not added to the dossier.
8. `pdftotext -layout temporary-primary-scan temporary-text`
   - Exit `0`.
   - Two scan pages inspected: exact theorem and complete prime/composite proof. OCR output was used
     for navigation, not as an independently reviewed transcription.
9. `lake env lean --version` with `cwd=Formalizations/Lean`
   - Exit `0`.
   - Lean 4.29.0, pinned commit and target recorded above.
10. `lake --version` with `cwd=Formalizations/Lean`
    - Exit `0`.
    - Lake 5.0.0-src+98dc76e; no update or build followed.
11. `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}`
    - Exit `0`; returned the pinned mathlib revision and tree above. Package status was clean.
12. `lake env lean ../../Stage1_Instances/THM-M-0931/IntakeProbe.lean` with
    `cwd=Formalizations/Lean`
    - Exit `0`.
    - All four public EGZ candidates elaborated. Complete output SHA-256:
      `40e2eb3a943f458ea70c1f1f77656878ee04fa3de9ddd56cf9f929ef4398b95f`.
      Each candidate reports `[propext, Classical.choice, Quot.sound]`. No canonical wrapper or
      theorem was declared by the probe.
13. `python3 -m json.tool` for `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root
    worker packet
    - Exit `0` for each file.
14. `python3 -B Stage1_Instances/THM-M-0931/check_intake.py --worker-packet .stage1-worker-selftest.json`
    - Exit `0`.
    - `intake invariant check: ok (THM-M-0931 planned; H1/M3/R4; six open tasks)`
15. `rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' Stage1_Instances/THM-M-0931`
    - Exit `1`, expected no-match result.
    - No prohibited proof escape or bodyless/unsafe declaration exists in the probe.
16. `git diff --check -- Stage1_Instances/THM-M-0931 .stage1-worker-selftest.json`
    - Exit `0`; no diagnostics. The scoped invariant checker separately checks untracked file bytes,
      final newlines, and trailing whitespace.
17. `git diff --no-index --check /dev/null PATH` for every new owned file and the worker packet,
    accepting exit `1` only when output is empty
    - Aggregate exit `0` after normalizing the expected new-file difference status.
    - No whitespace diagnostics for any untracked artifact.
18. `python3 -B Stage1_Instances/THM-M-0931/check_intake.py`
    - Exit `0` in public replay mode without the scheduler-only worker packet.
    - Rechecked the planned boundary and immutable inputs against the dossier alone.

## Result

The planned intake self-test passes with proposed vector `[H1, M3, R4]`. The primary scan and
pinned candidates are strong leads, but source admission, exact canonical target, formal proof and
release gates remain open. The provisional receipt is unsigned, non-content-addressed, dirty-tree
worker evidence pending master acceptance.
