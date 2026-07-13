# Intake validation record

## Scope

This record validates only the fail-closed `planned` intake for `S56-M-0963-INTAKE`: manifest
identity, dossier structure, theorem-family and non-substitution boundaries, source leads, the
open downstream DAG, and elaboration of adjacent pinned APIs plus an unproved candidate proposition
shape. It does not validate an exact canonical statement or any proof body.

The worker base is commit `a3b18eec39bf04be025b1641cae02f4d44fdf11a`, tree
`fdfff18dea4c6798c5b322b6088dfe556109c134`. Initial `git status --short` contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. It was preserved and used
read-only. The resulting intake files and worker packet make this nonrelease dirty evidence.

## Environment

- Linux `7.0.0-27-generic`, `x86_64`.
- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, release build.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its source worktree was clean.
- Dependency lock `Formalizations/Lean/lake-manifest.json`, SHA-256
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- No `lake update`, `lake build`, clone, fetch, or `.lake` mutation was run.

## Commands and results

1. `python3 Docs/tools/check_stage1_standard.py` exited `0`:
   `15` assurance groups, `41` legacy rows, `300` legacy slots, `1546` uniform-L0 targets,
   and skill presence passed.
2. `python3 scripts/stage1_target.py check` exited `0`: `1546` unique targets, contiguous
   ranks `1..1546`, all `L0/rework_required`.
3. `python3 scripts/stage1_target.py show THM-M-0963` exited `0`: rank `1497`, planned,
   no legacy slot, legacy artifacts unaccepted, theorem completion false.
4. `git status --short --untracked-files=all` and `git rev-parse HEAD HEAD^{tree}` exited `0`.
   The initial sole untracked input was the preserved `.lake` symlink; the recorded base and tree
   agree with this dossier.
5. `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and
   `git -C Formalizations/Lean/.lake/packages/mathlib status --short` exited `0`; the expected
   pin/tree were printed and status was empty.
6. `curl`/API metadata queries to zbMATH Open, arXiv, Crossref, Project Euclid, and the Osaka
   repository were used for bounded source discovery. zbMATH authenticated the primary
   bibliography; Project Euclid returned an access-block page and Osaka endpoints timed out, so no
   primary passage or PDF hash is claimed.
7. `curl -L --fail --silent --show-error https://arxiv.org/pdf/1512.05531v2`, the analogous
   commands for `0905.2423v2` and `2004.04937v2`, followed by `pdftotext -layout`, exited `0`.
   The observed PDF hashes and exact secondary locators are recorded in `instance.json` and the
   crosswalk. These are discovery inputs, not H0 evidence.
8. `rg -n -i --glob '*.lean'` over pinned mathlib and repository-local Lean for
   `Ray-Chaudhuri`, `L-intersecting`, and close lexical variants returned expected no-match
   results. This is bounded discovery only, not a downstream immutable anchor audit.
9. From `Formalizations/Lean`,
   `lake env lean ../../Stage1_Instances/THM-M-0963/IntakeProbe.lean` exited `0`.
   Seven adjacent APIs and `Stage1.THM_M_0963.Intake.CandidateTargetShape` elaborated; stdout
   SHA-256 was `58d9e070cd2e558e1e8770dfe19bd0e2cc16409cfa135d997067a09ca4478714`,
   stderr was empty. The probe declares no theorem or proof body.
10. `python3 -B Stage1_Instances/THM-M-0963/check_intake.py --worker-packet
    .stage1-worker-selftest.json` exited `0`: manifest and DAG identity, current hashes, null
    canonical target, H1/M3/R4 boundary, artifact inventory, packet, provisional receipt, and six
    open tasks agree.
11. `rg -n --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]'
    Stage1_Instances/THM-M-0963` exited `1`, the expected no-match result.
12. `PYTHONDONTWRITEBYTECODE=1 python3 -m json.tool` on all owned JSON and
    `python3 -B -m py_compile Stage1_Instances/THM-M-0963/check_intake.py` exited `0`;
    no bytecode artifact was retained in the owned path.
13. `git diff --check -- Stage1_Instances/THM-M-0963 .stage1-worker-selftest.json` exited `0`;
    per-untracked-file `git diff --no-index --check /dev/null <file>` returned only the expected
    new-file difference status and no whitespace diagnostics.

## Result boundary

The planned intake self-test passes and proposes worker state `[_]` for this intake item only.
Primary-source passage inspection, independent review, canonical statement selection, expression
and environment fingerprints, checked transports, statement mutations, candidate/provenance audit,
obligation graph, proof, trust closure, hermetic reproduction, independent validation, and master
acceptance remain open. `audit_complete` and `theorem_complete` are both false.
