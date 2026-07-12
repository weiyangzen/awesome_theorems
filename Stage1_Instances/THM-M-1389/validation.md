# Intake validation

Base revision: `02cc55f883d5b5d091ead6851bffe89199eb8391` (tree
`035212d041a1e61553b3d2f465964c9bbb35e47d`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope boundary, open task DAG, JSON and
scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical Weyl-law
statement or proof because neither has been frozen. The automation-provided canonical `.lake`
symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or other
`.lake` mutation was performed. This dirty worker evidence is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1389` | exit 0; rank 999, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10118,10123 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1007%2FBF01456804'` | exit 0; Crossref response SHA-256 `3b8011061aadab562a1469c089fd0c76c72a0bd8956651baee55465b9f594696`; identified the 1911 announcement chronology and 1912 PDE paper; discovery only |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1515%2Fcrll.1913.143.177'` | exit 0; Crossref response SHA-256 `920c24ce4defe4ab315d74613764ba7901bce9fe2ce2ba8dda4091b39ae010dc`; identified related 1913 bibliography; discovery only |
| `sha256sum` plus text inspection of temporary Teschl preliminary-edition and errata PDFs | exit 0; source hashes `362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e` and `3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`; located Theorem 5.25, equation (5.108); discovery only, no source admission or H0 credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1389/IntakeProbe.lean)` | exit 0; seven adjacent pinned asymptotic/spectral APIs elaborated; output SHA-256 `2ae8729c94c785976149ed3be161298cc11953cabf021cedd60103d96fef12dc`; no target theorem declared |
| bounded exact-topic `rg` search over pinned mathlib and repo-local Lean | exit 1; expected no match for Weyl-law, spectral-counting, or eigenvalue-asymptotic declarations; intake discovery rather than exhaustive audit |
| `python3 -m json.tool` on all owned JSON and the root worker packet | exit 0 after finalization |
| Python `ast.parse` on `check_intake.py` | exit 0; validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1389/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target/DAG identity, current source and dependency hashes, null target, H5/M4/R4 boundary, exact inventory, packet agreement, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for proof escapes or unsafe declarations |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection, repository-owned immutable primary-source admission, exact source
transcription and translation, complete incorporated definition/premise/conclusion/proof-boundary
and correction crosswalk, 1911/1912 chronology, historical-PDE-to-ODE relationship, and independent
source review remain open. So do the canonical Lean expression and environment fingerprints,
minimal imports, checked transports, statement mutations, exhaustive formal anchor audit, discovery
protocol, obligation registry, typed graphs, proof and composition, trust and provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
