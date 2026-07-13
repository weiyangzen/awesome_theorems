# Intake validation

Item: `S56-M-0979-INTAKE`

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a` (tree
`cc5285432a02107fadffb68c698690d1b98ac5f2`)

Validation date: `2026-07-13` (`Asia/Shanghai`)

This validation covers target membership, the planned dossier, duplicate and source-statement
boundaries, JSON integrity, the six-node open downstream DAG, and a narrow pinned Lean interface
and candidate-shape probe. It does not validate a canonical proposition, source acceptance,
statement fingerprint, proof, audit completion, or theorem completion. The automation-provided
canonical `.lake` link was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. The author-hosted source PDF was inspected only as
a temporary discovery input and was not added to the repository. This dirty worker run is
nonrelease evidence.

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

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0979` | 0 | rank 1513, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the automation-provided untracked `Formalizations/Lean/.lake` link; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base and tree recorded above |
| `git blame -L 7148,7153 -- Docs/researches/math_theorems.md` and duplicate-block blame | 0 | both uncited catalog blocks originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; title spelling alone prevents their exact-signature deduplication |
| author-hosted Vershynin second-edition PDF inspection with `sha256sum`, `pdfinfo`, and `pdftotext` | 0 | inspected Section 2.9 and bibliography leads in a 341-page, 5,634,501-byte PDF; SHA-256 `a5665ecf...0aac`; H1 discovery lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned dependency source remained clean |
| bounded exact-topic search in pinned mathlib and repository Lean | 0 | located MGF, Chernoff, sub-Gaussian, variance, and foreign `THM-M-0995` candidate surfaces; no separately named terminal scalar Bernstein tail theorem found; not a global absence claim |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0979/IntakeProbe.lean)` | 0 | pinned adjacent APIs and prefactor-parameterized candidate proposition elaborated; no theorem or proof body; stdout SHA-256 `caa6a4b8d61e829d1a406866b15dd86d0d9b216006bbd60382b951d32bae12e7` |
| `python3 -m json.tool` on owned structured JSON and the root worker packet | 0 | instance, task DAG, provisional receipt, and worker packet parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0979-pycache python3 -m py_compile Stage1_Instances/THM-M-0979/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0979/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, null target, H1/M3/R4 boundary, immutable inputs, duplicate boundary, exact inventory, packet agreement, and six open tasks passed; stdout SHA-256 `58c24a5ea7c45d6728c19d515c899d35eb235c4e920b81200668a12bb8f2a27c` |
| `python3 -B Stage1_Instances/THM-M-0979/check_intake.py` | 0 | public replay mode passed without requiring the scheduler-only root packet |
| prohibited Lean declaration scan over `IntakeProbe.lean` | 1 | expected no-match; no prohibited proof or trust-bypass declaration occurred |
| `git diff --check -- Stage1_Instances/THM-M-0979 .stage1-worker-selftest.json` plus scoped per-new-file checks | 0 | no whitespace diagnostics |

## Known open gates

Master acceptance of this intake is pending. The exact relationship to `THM-M-0995`, an admitted
historical or modern source edition, root selection, incorporated definitions, full premise and
constant mapping, genealogy, translation, corrections, errata, and independent source review are
open. So are the canonical Lean target, minimal imports, normalized expression and environment
fingerprints, checked transports, four statement mutation classes, exhaustive formal anchor and
terminal-body audit, discovery and obligation freezes, typed graphs, proof and composition,
readable reconstruction, trust closure, hermetic replay, deterministic bundle, independent
verification, audit completion, and theorem completion. These failures do not invalidate a
truthful self-tested `planned` intake.
