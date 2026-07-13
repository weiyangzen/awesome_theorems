# Intake validation

Base revision: `d1b510bacab792f84a99231485cf4429fdb78978` (tree
`f77c4e4db196fc0ecc271815514a411d06ea6053`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement ambiguity, empty-space and
non-substitution boundaries, open task DAG, structured intake invariants, and a narrow pinned Lean
API probe. It does not validate a canonical Baire-category proposition or target proof because
neither has been frozen. The automation-provided canonical `.lake` symlink was pre-existing and
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was performed.
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

All commands were run from the repository root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0631` | 0 | rank 1324; planned; L0/rework required; no legacy slot; legacy artifacts unaccepted; theorem complete false |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit and tree shown above |
| `git blame -L 4678,4683 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over the manifest, blueprint, execution DAG, skill, guidelines, source corpus, Stage0, toolchain, lockfile, and five pinned Baire/category sources | 0 | hashes recorded in `instance.json` and checked by `check_intake.py` |
| `curl -L --fail --max-time 20 -sS https://api.crossref.org/works/10.1007/BF02419243` | 0 | 4113-byte response, SHA-256 `5c7aede997927a012832dec67e0b6357a2aca2918305604f512d419e77af4c85`; identifies Baire's 1899 paper, but no theorem-level source credit |
| `curl -L --fail --max-time 40 -A Mozilla/5.0 -sS https://link.springer.com/article/10.1007/BF02419243` | 0 | 217743-byte landing page, SHA-256 `b9a74acab6c1b794abab29c0c0161d53b9db7ed984d7c55da9e55242f12b6341`; bibliographic lead only |
| advertised Springer PDF endpoint | 0 transport | returned 217777 bytes of HTML, not a PDF; response SHA-256 `20fde7ee5101751a4f9b303f7d99571ca2cdc99c436baaa4b33e63ee2ff04421`; no primary theorem pages obtained |
| `lake env lean --version` (`cwd=Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `lake --version` (`cwd=Formalizations/Lean`) | 0 | Lake 5.0.0-src+98dc76e; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package source clean |
| bounded exact-topic `rg` inspection of repo-local Lean and pinned mathlib | completed | located the complete-(pseudo)metrizable Baire instance, category definitions/lemmas, and the distinct locally compact theorem; intake discovery only |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0631/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | 0 | eleven interfaces elaborated; `BaireSpace Empty` synthesized; `Set.univ : Set Empty` checked meagre; candidate instance axioms were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `f15310c589d3edeff1ed2582ba4b11db365853276f95a50bf4e0928362b585ea` |
| `python3 -m json.tool` on all structured owned JSON and the root worker packet | 0 | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0631-pycache python3 -m py_compile Stage1_Instances/THM-M-0631/check_intake.py` | 0 | validator compiled without generated files in the owned path |
| `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0631/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, null target, H1/M3/R4 boundary, pins, artifact hashes, provisional receipt, packet, empty-space probe, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 expected | no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations |
| scoped untracked-file whitespace checks plus `git diff --check` | 0 | no whitespace errors |

## Known open gates

An accepted primary or authoritative source edition, exact theorem locator and proposition,
Baire-space-versus-whole-space decision, metric/pseudometric/topological domain, separation and
nonemptiness premises, category encoding, binders, conclusion, boundary cases, translation and
errata audit, and independent source review remain open. So do the canonical Lean expression and
environment fingerprints, minimal imports, checked transports, statement mutations, exhaustive
formal anchor audit, discovery protocol, obligation registry, typed graphs, proof and composition,
provenance and trust closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion. These open
gates do not invalidate a truthful self-tested `planned` intake.
