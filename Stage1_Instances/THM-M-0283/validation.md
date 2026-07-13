# Intake validation

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702` (tree
`02279a8caa5f31ed8e37e35c8584a336eed9b974`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope crosswalk, open task DAG, structured
invariants, and pinned Lean candidate probe. It does not validate a canonical Markov proposition or
proof because exact source identity and statement freeze remain open. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no update, build, clone, fetch, or
other dependency mutation was performed. Dirty worker evidence is nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- Lean executable SHA-256:
  `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0283` | exit 0; rank 1289, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| repository source/blame and duplicate-record inspection | exit 0; two identical uncited catalogue records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; neither supplies an exact statement or bibliography |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0283/IntakeProbe.lean)` | exit 0; measure/lintegral plus four exact-topic Markov declarations elaborated; all four candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `0820c158f5436f5e120a2561389c150994d5933e5ca1ba5c3159ea9811dd428d` |
| bounded `rg` search in pinned mathlib and repo-local Lean | exit 0; exact-topic ENNReal and real-integral declarations and adjacent uses located; no source-identical root transport credited; intake discovery only |
| `python3 -m json.tool` on the structured intake artifacts | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0283-pycache python3 -m py_compile Stage1_Instances/THM-M-0283/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0283/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H1/M3/R4 boundary, duplicate source and dependency pins, artifact inventory, worker packet, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no declaration-token match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` in the API-only probe; this intentionally permits the trusted diagnostic command `#print axioms` |
| scoped new-file whitespace checks and `git diff --check` | no diagnostics; `git diff --no-index --check` returns 1 only because each new file differs from `/dev/null`, while whitespace diagnostics are empty |

## Known open gates

Canonical root selection, a primary or authoritative source edition and locator, complete source
definition and assumption reconstruction, proof boundary, corrections and errata audit, and
independent source review remain open. So do the measure and value codomains, nonnegativity,
measurability, integrability, threshold, event, bound-form and boundary decisions; canonical Lean
expression and environment fingerprints; checked transports and statement mutations; exhaustive
anchor and provenance audit; discovery protocol; obligation registry; typed graphs; proof and
composition; trust closure; readable reconstruction; hermetic replay; deterministic bundle;
independent verification; master acceptance; audit completion; and theorem completion. These
failures do not invalidate a truthful self-tested `planned` intake.
