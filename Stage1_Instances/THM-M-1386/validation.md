# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof because the catalog does not select one
binder-complete source result.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The publisher PDF of Paul R. Beesack's *On Sturm's Separation Theorem*, *Canadian Mathematical
Bulletin* 15(4) (1972), pp. 481-487, DOI `10.4153/CMB-1972-086-7`, was inspected as a temporary
worker input. The 730,959-byte, seven-page PDF has SHA-256
`5a7480ce6690550fe5fa545166943b33f7faddf9dbccb6eddb9918aea71e1ce9`.

Page 481's classical summary and Theorem 1 on pages 481-483 establish a close source-family match,
but also expose proposition-changing choices between a compact theorem and singular-endpoint
extensions. The publisher page displayed no article-specific correction/retraction marker, and a
bounded Crossref relation/update check was empty. This is not a global no-errata claim. The PDF was
not added to the repository, and no immutable source admission, complete premise/proof/errata
mapping, historical-source chain, or independent H0 review is claimed.

## Environment fingerprint

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1386` | 0 | rank 996; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 10097,10102 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| publisher PDF download and `pdftotext -layout` inspection | 0 | Beesack classical summary and Theorem 1 inspected; observed size/pages/digest recorded above; temporary discovery input only |
| bounded publisher-page and Crossref correction/relation inspection | 0 | no article-specific correction marker or Crossref update/relation located; bounded observation only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1386/IntakeProbe.lean)` | 0 | eight adjacent pinned APIs elaborated; complete output 2,143 bytes, SHA-256 `08fbf7036a959b8b77588d2f4855706f17f7dcf59bd2d489e1279ec34cd7650f`; no target declaration or proof body |
| `rg -n -i --glob '*.lean' 'sturm\|wronskian\|interlac' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | matches were polynomial Wronskian material, an unrelated Stage1 comment, and no functional Sturm-separation target; bounded intake discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1386/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1386/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H1/M4/R4 null target, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1386/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1386 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; per-file no-index checks cover untracked artifacts |

## Known downstream failures

- The catalog does not select the classical compact theorem, Beesack Theorem 1(b), the full
  singular-endpoint extension, or another exact source result, and it supplies no historical source.
- Equation form, interval and endpoint model, coefficient and solution regularity, scalar field,
  independence and consecutive-zero encodings, interlacing strength, quantifier order, exact
  conclusion, and boundary cases remain open.
- No canonical Lean expression, exact minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- The API probe is adjacent substrate only. Formal anchor audit, discovery and obligation freezes,
  typed graphs, proof, composition, trust closure, readable reconstruction, hermetic replay,
  deterministic bundle, independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the source and scope
ambiguity and open the downstream DAG. Only the integration lane may accept the provisional worker
receipt.
