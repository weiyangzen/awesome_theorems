# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family and duplicate discrimination, JSON and scoped invariants, a narrow pinned
Lean substrate probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and
whitespace. It does not validate a canonical theorem statement or proof because the catalog does
not select one exact Gilbert-Varshamov proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

A complete scan of *Bell System Technical Journal* 31(3), May 1952, was downloaded to temporary
worker storage and inspected. E. N. Gilbert's *A Comparison of Signalling Alphabets*, printed
pages 504-522, contains Theorem 1 and its greedy lower-bound proof at printed pages 506-507. The
9,411,506-byte issue scan has SHA-256
`beb31559049787510a90aba8a3a8ab48f753e0e3b2df2fe2fb4bf1e53a536431`; an eight-page text
extract has 20,965 bytes and SHA-256
`ffaa6242a6f3752387c33495a65e5f9a2c5b84a22bf77925e32ae07a43157663`.

The source supports family discrimination and provisional H1 only. The catalog does not cite or
select it, no primary Varshamov source was admitted, no source file was added to the repository,
and no lawful immutable archive, canonical transcription, errata audit, complete boundary mapping,
or independent H0 review is claimed.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1588` | 0 | rank 1028; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 11700,11705 -- Docs/researches/math_theorems.md` | 0 | all six mathematical catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| download of the Bitsavers Bell System Technical Journal issue to temporary storage | 0 | 202-page, 9,411,506-byte PDF with the digest recorded above; not added to the repository |
| `pdftotext -f 96 -l 103 -layout <temporary-Gilbert-issue-scan> <temporary-extract>` | 0 | extracted 20,965 bytes; inspected Gilbert Theorem 1 and proof at printed pages 506-507 |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1588/IntakeProbe.lean)` | 0 | eight Hamming, finite-cardinality, binomial, and finite-maximum APIs elaborated; complete output SHA-256 `1ed540134a5139c734485852b9fbaa0587938ac505e85ae987446a1736c4d8bf` |
| bounded exact-topic search over pinned mathlib and repo-local Lean | 0 | only mathlib's prose phrase "minimum distance" matched; no Gilbert/Varshamov or terminal code-bound declaration found; discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1588/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1588/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, source/duplicate boundaries, inventory, packet, hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1588/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1588` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1588 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The catalog does not choose the finite binary, finite q-ary nonlinear, linear Varshamov, or
  asymptotic entropy-rate formulation.
- The inspected Gilbert paper is neither catalog-cited nor independently admitted to H0, and a
  primary Varshamov source and exact relationship are absent.
- The parallel Stage0-only `THM-C-0372` record uses the date 1952-57; duplicate identity and
  ownership remain unresolved.
- Alphabet, code model, length, distance, dimension or rate, ball-volume radius, rounding,
  parameter ranges, binder order, conclusion, and all degenerate cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
