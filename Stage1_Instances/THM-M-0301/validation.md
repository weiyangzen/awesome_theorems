# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, exact repository and probable-duplicate boundaries,
the inspected primary announcement, the six-node open downstream DAG, JSON and scoped invariants,
and a narrow pinned Lean API probe. It does not validate a canonical BMO-duality Lean statement or
proof because the proposition-changing source choices and concrete analytic foundations remain
open. The automation-provided canonical `.lake` symlink was pre-existing and used read-only; no
dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker
evidence is nonrelease evidence.

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
- Inspected Fefferman 1971 AMS PDF SHA-256:
  `7352edb3d25ffcfd7473ad738751b5e0d8e7dccd13540b45a57647289405524d`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0301` | exit 0; rank 1047, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 2160,2165 -- Docs/researches/math_theorems.md` | exit 0; all six uncited target lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 2640,2645 -- Docs/researches/math_theorems.md` | exit 0; the probable duplicate `THM-M-0363` source lines originate at the same commit |
| inspection of Fefferman, *Characterizations of bounded mean oscillation*, AMS 1971 PDF, page 587 | exit 0; BMO definition, quotient by constants, Theorem 1, integral pairing, and adjacent Riesz-transform `H^1` description were inspected; no H0 acceptance |
| `file /tmp/fefferman1971.pdf` and `sha256sum /tmp/fefferman1971.pdf` | exit 0; valid two-page PDF with the source digest recorded above |
| Crossref DOI lookup for `10.1090/S0002-9904-1971-12763-5` | exit 0; author/title/year/pages agreed and `relation` was empty; this is not a comprehensive errata audit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0301/IntakeProbe.lean)` | exit 0; seven adjacent pinned APIs elaborated; no target theorem declared |
| word-bounded exact-topic `rg` search for bounded mean oscillation, BMO, Hardy space, HardySpace, Riesz transform, and RieszTransform in pinned mathlib | exit 0 only for four unrelated local variables named `Bmo`; no concrete target API found; bounded intake discovery, not exhaustive anchor audit |
| corresponding exact-topic `rg` search in repo-local Lean and the read-only `THM-M-0363` dossier | exit 0 only for `THM-M-0363` probe prose; no target proof body found |
| `sha256sum` on the manifest, blueprint, execution DAG, skill, guidelines, source record, Stage0 projection, toolchain, and lock file | exit 0; immutable input hashes recorded in `instance.json` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0301-pycache python3 -m py_compile Stage1_Instances/THM-M-0301/check_intake.py` | exit 0; validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0301/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authority identity, null exact target, H1/M4/R4 boundary, source and duplicate pins, exact artifact inventory and hashes, provisional receipt/worker packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations |
| scoped `git diff --check` plus validator newline/whitespace checks | exit 0; no whitespace errors in tracked or untracked owned artifacts |

## Known open gates

A complete immutable proof source, all norm and normalization choices, comprehensive errata audit,
pinpoint proof-node mapping, `THM-M-0363` duplicate reconciliation, and independent source review
remain open. So do the canonical Lean expression and environment fingerprints, concrete Euclidean
BMO and real `H^1` foundations, checked transports, statement mutations, exhaustive formal anchor
audit, discovery protocol, obligation registry, typed graphs, proof and composition, trust and
provenance closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion. These downstream
failures do not invalidate a truthful self-tested `planned` intake.
