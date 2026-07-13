# Intake validation

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702` (tree
`02279a8caa5f31ed8e37e35c8584a336eed9b974`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope crosswalk, open task DAG, structured
invariants, and pinned Lean candidate probe. It does not validate a canonical Jensen proposition
or proof because source variant selection and statement freeze remain open. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no update, build, clone, fetch, or
other dependency mutation was performed. Dirty worker evidence is nonrelease.

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
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0281` | exit 0; rank 1287, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 2020,2025 -- Docs/researches/math_theorems.md` | exit 0; all six sparse catalog lines originate at `bcf3f9fa...` |
| `curl -L --fail --silent --show-error --max-time 30 -H 'User-Agent: awesome-theorems-stage1/5.6' 'https://api.crossref.org/works/10.1007/BF02418571'` plus `sha256sum` | exit 0; 3834-byte response, SHA-256 `a82ca423...f7dba`; matching Jensen 1906 metadata located; full article text was not admitted, so no pinpoint theorem or H0 claim |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0281/IntakeProbe.lean)` | exit 0; eight integral, average, finite, concave, strict, and equality-case Jensen interfaces elaborated; both candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `916d4f48a8cb821d7ff8e4bc1a9ed45b4dadc90820233feec8b44922aed577ea` |
| bounded `rg -n -i 'Jensen.?s inequality\|map_integral_le\|map_average_le\|map_set_average_le\|map_centerMass_le\|map_sum_le'` over repo-local Lean and pinned `Mathlib` | exit 0; exact-topic pinned integral, finite, strict, and conditional families located; no pre-existing target dossier or source-identical transport credited; intake discovery only |
| `python3 -m json.tool` on the structured intake artifacts | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0281-pycache python3 -m py_compile Stage1_Instances/THM-M-0281/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0281/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H1/M3/R4 boundary, source and dependency pins, artifact hashes, worker packet, validation actions, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0281/check_intake.py` | exit 0 after finalization; public replay mode passed without the root packet |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no declaration-token match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` in the API-only probe; this intentionally permits diagnostic `#print axioms` |
| `git diff --check -- Stage1_Instances/THM-M-0281 .stage1-worker-selftest.json` and a per-file loop of `git diff --no-index --check /dev/null <file>` over every changed file | exit 0; each no-index command returned its expected new-file status 1 with empty diagnostics, and no whitespace error was found |

## Known open gates

Canonical root selection, complete primary-source definition and assumption reconstruction,
translation, correction and errata audit, and independent source review remain open. So do the
canonical Lean expression and environment fingerprints, checked integral/average/finite and
convex/concave transports, statement mutations, exhaustive anchor and provenance audit, discovery
protocol, obligation registry, typed graphs, proof and composition, trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
