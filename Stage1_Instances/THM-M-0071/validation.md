# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers manifest membership, the fail-closed dossier and open task DAG, repository
provenance, bounded source discrimination, JSON and scoped invariants, a narrow pinned Lean branch
probe, proof-escape hygiene, and whitespace. It does not validate a canonical CFSG proposition or
proof because the exact representative taxonomy and primary proof-source boundary are not frozen.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Source discovery boundary

Tatitscheff's *A short introduction to Monstrous Moonshine*, arXiv `1902.03118v4`, was inspected as
a versioned secondary statement witness. Theorem 1 on printed PDF page 2 gives the literal
18-infinite-family or 26-sporadic alternative; the adjacent paragraph counts prime cyclic and
alternating groups plus 16 Lie-type families. The 190,670-byte PDF has SHA-256
`d7a471c813f8d21383c9ac5ff1cdffd58f1a43f1346e872d350a16e06a19eb6c`; the observed arXiv metadata
response has SHA-256 `e84ba46ff664fc3c715f361545b8990be6bcd1add4c14d94fcf06b7c162a4246`.
The exposition is not catalog provenance or primary proof evidence, leaves incorporated definitions
and formal taxonomy unresolved, and dates completion to 2004 with a 2008 correction. It receives
`E5` discovery status only.

Gorenstein's 1983 Volume 1 was inspected as a primary-book proof-boundary lead. Its Conclusion,
page 475 and DOI suffix `_7`, gives the noncharacteristic-2 reduction to a characteristic-2-type
minimal counterexample whose proper subgroups are K-groups. This is not a self-contained terminal
18/26 proof. The inspected front- and back-matter PDF digests are
`9fc1ad7670dcf338af111a52be0012940032999182095a0d1408a37348928743` and
`12fcea8e5a52f3dade2d8426f99e8a21ee0b2f822cae76b65159ebc8de986e4a`. No external source was
copied into the repository; no source was admitted as `H0` or independently reviewed.

## Environment fingerprint

- Platform: Linux x86_64; kernel `7.0.0-27-generic`; timezone `Asia/Shanghai`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

Commands ran from the repository root on 2026-07-13 Asia/Shanghai unless another `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0071` | 0 | rank 1016; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 526,531 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| versioned Tatitscheff PDF download and `pdftotext -f 1 -l 4 -layout` to temporary files | 0 | Theorem 1, family-count paragraph, 190,670 bytes, and the PDF digest above were inspected; discovery input only |
| Gorenstein book, Introduction, and Conclusion publisher-metadata/page inspection | 0 | 1983 book identity and page-475 noncharacteristic-2 reduction confirmed; no terminal proof ledger credited |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake agree with the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0071/IntakeProbe.lean)` | 0 | nine adjacent APIs elaborated; complete stdout 1,089 bytes, 13 lines, SHA-256 `a0cc26767186f6c4e43b2bd8b9ed22c5a97cdf05aa5ab3ffb00733a3b328ba5c` |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 (expected no match) | no terminal exact-topic declaration under the recorded patterns; intake discovery only, not a complete audit or global absence claim |
| `python3 -m json.tool` on all owned JSON artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0071/check_intake.py` | 0 | scoped validator parses without generated bytecode |
| `python3 -B Stage1_Instances/THM-M-0071/check_intake.py` | 0 | durable public recipe: target, source pins, H1/M4/R4 planned boundary, null target, artifacts, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0071/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | scheduler handoff additionally agrees with the dossier and provisional receipt |
| prohibited-construct scan over owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` and scoped `git diff --check` | 0 aggregate | no whitespace diagnostics, including untracked files |

## Known downstream failures

- No independently reviewed immutable primary proposition, incorporated definitions, assumptions,
  correction history, complete proof boundary, or source-to-node mapping is frozen.
- The exact simple-group and isomorphism conventions, 18-family roster, parameter and exclusion
  ledger, quotient choices, exceptional isomorphisms, all 26 representatives, Tits-group treatment,
  and exhaustiveness-versus-uniqueness conclusion remain open.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
