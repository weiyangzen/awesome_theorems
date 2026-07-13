# Intake validation

Base revision: `f294137feee7840fd105a4d3f6073d5cf45508ea` (tree
`234b8f273d252c2c42ce6860315ed973049c871a`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope crosswalk, open task DAG, structured
invariants, and pinned Lean candidate probe. It does not validate a canonical Vitali proposition,
root bundle, covering-to-differentiation composition, or proof because source and statement
selection remain open. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only; no update, build, clone, fetch, or other dependency mutation was performed. Dirty worker
evidence is nonrelease.

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
| `python3 scripts/stage1_target.py show THM-M-0288` | exit 0; rank 1294, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| Crossref/Zenodo inspection for DOI `10.1007/BF03014093` | exit 0; matching 1904 article metadata and eleven-page open scan located; its focus does not identify the modern compound root, so it remains an H1 lead |
| zbMATH document `2639907` and Encyclopedia of Mathematics revision `55740` inspection | exit 0; contemporary JFM metadata/review authenticates the 1908 article and interval-family/application relationship; the primary text remains unavailable and the two records conflict on pagination, so neither supplies H0 or an exact target |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0288/IntakeProbe.lean)` | exit 0; ten representative covering, Vitali-family, measure-differentiation, density, and function-average signatures elaborated; five axiom reports were `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `c7cb70922146dc629842ee69d6d66b791359a44af65ef59093b09e2170ae5ce3` |
| bounded `rg` search in pinned mathlib and repo-local Lean | exit 0; multiple inequivalent exact-topic pinned declarations located and no source-identical repo-local root found; intake discovery only, not the exhaustive anchor audit |
| `python3 -m json.tool` on structured intake artifacts | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0288-pycache python3 -m py_compile Stage1_Instances/THM-M-0288/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0288/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H1/M3/R4 boundary, source and dependency pins, artifact hashes, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0288/check_intake.py` | exit 0 after finalization; public replay mode passes without the scheduler-only worker packet |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no declaration-token match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` in the API-only probe; the diagnostic command `#print axioms` is intentionally permitted |
| scoped new-file whitespace checks and `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root or bundle selection, immutable primary-source admission, complete source definitions
and assumption reconstruction, exact historical-to-modern translation, correction/errata audit,
and independent source review remain open. So do the canonical Lean expression and environment
fingerprints, exact minimal imports, checked alternate encodings and covering-to-differentiation
composition, statement mutations, exhaustive anchor and terminal-body provenance audit, discovery
protocol, obligation registry, typed graphs, proof and composition, trust closure, readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, and
master acceptance.

The first downstream failed gate is `S56-M-0288-STATEMENT`: the catalogue's compound gloss does not
select an exact source proposition or explicit root bundle. This planned intake is nevertheless
self-tested for its own bounded deliverable. It remains provisional `[_]`, not accepted `[x]`.
