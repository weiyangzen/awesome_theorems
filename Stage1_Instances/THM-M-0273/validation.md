# Intake validation

Base revision: `d3cbfa8941a8bcaafa3b8a690d1333f9643288ad` (tree
`e912a107150c6f9c3fc096901412fce0337c7c01`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, primary-source and scope crosswalk, open task DAG,
structured invariants, and pinned Lean candidate probe. It does not validate a canonical Radon-
Nikodym proposition or proof because source variant selection and statement freeze remain open. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no update, build,
clone, fetch, or other dependency mutation was performed. Dirty worker evidence is nonrelease.

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
| `python3 scripts/stage1_target.py show THM-M-0273` | exit 0; rank 1020, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| publisher/Crossref inspection for DOI `10.4064/fm-15-1-131-179` | exit 0; matching 1930 paper and 25-page image-only scan located; printed Theorem III, page 168, inspected as an H1 lead, not admitted as H0 |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0273/IntakeProbe.lean)` | exit 0; ten positive/signed measure, decomposition, density, and Radon-Nikodym interfaces elaborated; all three candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `26c7f8d7155beccf566ea4e2abafbda72a412ff3f9b9576c37b49be8c3a4aebb` |
| bounded `rg` search in pinned mathlib and repo-local Lean | exit 0; exact-topic pinned declarations and adjacent uses located; no source-identical root transport credited; this was intake discovery, not the later exhaustive anchor audit |
| `python3 -m json.tool` on the structured intake artifacts | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0273-pycache python3 -m py_compile Stage1_Instances/THM-M-0273/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0273/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H1/M3/R4 boundary, source and dependency pins, artifact hashes, worker packet, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no declaration-token match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` in the API-only probe; this intentionally permits the trusted diagnostic command `#print axioms` |
| scoped new-file whitespace checks and `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection, complete primary-source definition and assumption reconstruction, exact
historical-to-modern translation, correction/errata audit, and independent source review remain
open. So do the canonical Lean expression and environment fingerprints, checked positive/signed
and implication/iff transports, statement mutations, exhaustive anchor and provenance audit,
discovery protocol, obligation registry, typed graphs, proof and composition, trust closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
