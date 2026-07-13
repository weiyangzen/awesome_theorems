# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants,
repository-source provenance, pinned environment identity, a narrow Lean API probe, a bounded
local search, proof-escape hygiene, JSON integrity, and whitespace. The source gloss is not a
truth-valued proposition. Elaborating a purported canonical target would prematurely choose a side
or angle rule, sphere and radius, side and angle encodings, arc and orientation conventions,
triangle validity, and boundary cases. `IntakeProbe.lean` therefore checks adjacent APIs only and
supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux x86_64; worker timezone `Asia/Shanghai`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0214` | 0 | rank 1229, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 1543,1548 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1543,1548p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `e9574d1caf262cd04ec9029e4692be1a8f5b76068de537aa25e81ef9c8e721c9` |
| `sed -n '5946,5971p' Docs/Stage0_Blueprint.md \| sha256sum` | 0 | exact Stage0 block SHA-256 `d02734bdba61dfdf0e7d7bb39200e89986445a0fa98ace32ee7441e473c084a4` |
| `curl -L --fail --max-time 30 -sS 'https://mathworld.wolfram.com/SphericalTrigonometry.html' -o /tmp/spherical_mathworld.html` | 0 | retrieved 103,608-byte mutable secondary discovery page; cyclic side and dual angle rules inspected; no H evidence admitted |
| `curl -L --fail --max-time 30 -sS 'https://encyclopediaofmath.org/wiki/Spherical_trigonometry' -o /tmp/spherical_eom.html` | 0 | retrieved 19,064-byte mutable secondary discovery page; both cosine-rule families and the central-angle/arc-length convention inspected; no H evidence admitted |
| `sha256sum /tmp/spherical_mathworld.html /tmp/spherical_eom.html` | 0 | response SHA-256 values `adb9e1af40ddc3c7bdcda48e08a77cb4949c159a1cfe688f01819cbd18dd00d0` and `4d2e24b24bed1b949306af5b4cc88c7a6d58e3d84ba66c07821f48c8a7c6ecff`; snapshots remain temporary discovery evidence, not archived H evidence |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 and Lake 5.0.0 at the recorded Lean revision |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 each | pinned revision and tree above; status output empty, so the package worktree was clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0214/IntakeProbe.lean)` | 0 | ten pinned ambient-sphere, angle, inner-product, Euclidean-law, and trigonometric APIs elaborated; no target declaration |
| `rg -n -i --glob '*.lean' 'spherical.{0,50}(law\|cos)\|(?:law\|cos).{0,50}spherical\|spherical triangle' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | matches were only the unrelated substring `cospherical` in ambient Euclidean sphere files; no spherical-triangle or spherical-law declaration found; bounded intake discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool Stage1_Instances/THM-M-0214/instance.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-0214/task-dag.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-0214/intake-receipt.json >/dev/null && python3 -m json.tool .stage1-worker-selftest.json >/dev/null` | 0 | all structured records are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0214-pycache python3 -m py_compile Stage1_Instances/THM-M-0214/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0214/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, pinned inputs, H5/M4/R4 planned boundary, null target, exact artifact inventory, worker packet, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-0214/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet and remains valid after provisional DAG integration |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)[[:space:]]\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0214` | 1 | expected no-match result; no proof escape declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0214 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null <file>` for every new file | 0 | no whitespace diagnostics; the intake checker separately rejects CR, NUL, missing final newline, and inventory mismatch |

The provisional receipt binds each non-self-referential new dossier artifact by SHA-256. Its own
bytes and the root scheduler handoff are explicitly excluded because neither file can contain its
own final digest. Both remain mutable, non-content-addressed worker evidence and must be recaptured
by the integration lane; this intake makes no release-receipt claim.

## Known downstream failures

- The catalog wording is not a stable proposition. No approved source selects the side rule, dual
  angle rule, cyclic family, equivalence, or another exact relation.
- No independently reviewed immutable primary or authoritative theorem, complete
  definition/assumption/proof/errata crosswalk, or exact source locator is accepted.
- Sphere dimension and radius, central-angle or arc-length side convention, selected geodesic arcs,
  angle and orientation convention, triangle validity, binder order, hypotheses, conclusion, and
  degenerate cases remain open.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  alternate encoding, or semantic mutation test exists.
- Discovery precommit, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification remain open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose deliverable is to freeze this ambiguity boundary and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
