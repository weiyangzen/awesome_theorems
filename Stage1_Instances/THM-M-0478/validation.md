# Intake validation

Base revision: `0f70149d61a952d44f907f4662a143372bcb4c44` (tree
`35328e4f56f47446a4e1dfdbe361a1b70a4b18a7`). Validation date: 2026-07-13
(`Asia/Shanghai`).

This validation covers target membership, the planned dossier and open DAG, source-statement and
non-substitution boundaries, source provenance, structured intake invariants, and one narrow pinned
Lean discovery probe. The probe authenticates candidate theorem interfaces and reports their
axioms; it does not select or elaborate a canonical target, inspect terminal proof provenance, or
grant proof credit. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was performed.
This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0478` | exit 0; rank 1359, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 3511,3516 -- Docs/researches/math_theorems.md` | exit 0; all six catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://gdz.sub.uni-goettingen.de/fulltext/PPN235993352/00000103.xml | sha256sum` | exit 0; Article 131 Latin-source OCR XML digest `77d05ec702c806064b3d4a3b5494a4bc4b7989445c26278bdb132ab7b1c80809` |
| `curl -L --fail --silent --show-error https://gdz.sub.uni-goettingen.de/fulltext/PPN373456743/00000106.xml | sha256sum` | exit 0; Article 131 German-translation OCR XML digest `7d5e59b7d9db4bdb263b871a1ddf8df37c752c089004bde2ccf3d7ca9034d6e8` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0478/IntakeProbe.lean` | exit 0; seven declarations elaborated; product and equality candidates both report `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `775d93407ed1b75f73dc6640374d2a1dcc6625f5bf9c6d80234daea5baf35a9a` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after final serialization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0478-pycache python3 -m py_compile Stage1_Instances/THM-M-0478/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0478/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; authority identity, pins, null canonical target, H1/M3/R4 boundary, source/formal leads, artifact hashes, provisional receipt, worker packet, and six open tasks agree |
| prohibited Lean declaration scan over `IntakeProbe.lean` | exit 0; inner `rg` returned expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration was found |
| `git diff --check -- Stage1_Instances/THM-M-0478 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null` for each untracked owned file | no whitespace diagnostics; each no-index command returned 1 only because the new file differs from `/dev/null` |

## Validation boundary

The candidate axiom output is an observation, not accepted foundation or transitive trust closure.
The source downloads were bounded intake inspection; neither mutable OCR endpoint is archived or
accepted as an H0 source. The receipt and worker packet are unsigned, non-content-addressed,
nonrelease proposals pending independent integration-lane replay and master acceptance.

The exact source proposition, approved transcription and translation, definition chain, domains,
binders, prime/odd/distinctness premises, Legendre-symbol convention, sign, orientation, equality
case, corrections, and independent source review remain open. So do the canonical Lean expression
and environment fingerprints, checked transports, statement mutations, exhaustive anchor audit,
discovery and obligation freezes, typed graphs, proof, composition, trust and provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, audit
completion, and theorem completion. These open gates do not invalidate a truthful self-tested
`planned` intake.
