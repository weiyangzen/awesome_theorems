# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`; base tree:
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, bibliographic identity, source-family and duplicate discrimination, JSON and scoped
invariants, a narrow pinned Lean substrate probe, a bounded repo-local and mathlib search,
prohibited-construct hygiene, and whitespace. It does not validate a canonical theorem statement
or proof because the catalog does not select one exact Singleton proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref and DBLP metadata confirm Richard C. Singleton, *Maximum distance q-nary codes*, **IEEE
Transactions on Information Theory** 10(2), April 1964, pages 116-118, DOI
`10.1109/TIT.1964.1053661`. The Crossref response had SHA-256
`262f9ef840614ff7c57fef1665ac766dc555ed84536bc2109cf68e015e9dedff`; the DBLP BibTeX response
had SHA-256 `c6c39601fdfaf2f5817e4d02f9e1e17b7b4ad54ee62393f9b2a7516d4cea5630`.
Unpaywall reported closed access and no repository copy; its response had SHA-256
`b09a0a0b08533555b0e5a3080bb44e8ce6f564545a58c15f6f844bf0638b8ebe`. An IEEE paper download
attempt returned an access response rather than the paper. No paper text or theorem transcription
was admitted.

For scope discrimination only, the 4,838-byte Error Correction Zoo `mds.yml` at immutable
revision `1fcaa85f447bff9c77a6c33595ee4c72548d5d85` was inspected. Its SHA-256 is
`a3c8816a587bfa0086174d94da2056d74480b0bbeb371da191ccd070fddf32a7`. It distinguishes a linear
MDS equality case from a general unrestricted q-ary bound. It is modern secondary metadata, not
primary proof evidence or target authority.

These sources support family discrimination and provisional H1 only. The catalog does not cite or
select the primary paper; the paper text, exact proposition, proof, assumptions, corrections,
errata, complete boundary mapping, and independent H0 review remain open.

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
| `python3 scripts/stage1_target.py show THM-M-1587` | 0 | rank 1209; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 11693,11698 -- Docs/researches/math_theorems.md` | 0 | all six mathematical catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 https://api.crossref.org/works/10.1109/TIT.1964.1053661` | 0 | 2,975 bytes; SHA-256 `262f9ef840614ff7c57fef1665ac766dc555ed84536bc2109cf68e015e9dedff`; exact bibliography confirmed |
| `curl -L --fail --silent --show-error --max-time 30 https://dblp.org/rec/journals/tit/Singleton64.bib` | 0 | 580 bytes; SHA-256 `c6c39601fdfaf2f5817e4d02f9e1e17b7b4ad54ee62393f9b2a7516d4cea5630`; DBLP bibliography confirmed |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.unpaywall.org/v2/10.1109/TIT.1964.1053661?email=codex%40openai.com'` | 0 | 904 bytes; SHA-256 `b09a0a0b08533555b0e5a3080bb44e8ce6f564545a58c15f6f844bf0638b8ebe`; closed access and no repository copy reported |
| `curl -L --fail --silent --show-error --max-time 60 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1053661' -o /dev/null` | 22 | HTTP 418 access response; no paper bytes obtained and no source-text claim made |
| `curl -L --fail --silent --show-error --retry 2 --max-time 90 https://raw.githubusercontent.com/errorcorrectionzoo/eczoo_data/1fcaa85f447bff9c77a6c33595ee4c72548d5d85/codes/classical/q-ary_digits/distributed_storage/mds.yml` | 0 | 4,838 bytes; SHA-256 `a3c8816a587bfa0086174d94da2056d74480b0bbeb371da191ccd070fddf32a7`; modern scope discriminator only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1587/IntakeProbe.lean)` | 0 | eight Hamming and finite-cardinality APIs elaborated; complete output SHA-256 `a3547fa913bcfd9addfd9938fbbbd94e3d322c55eea4efa8948de94a6a7dc814` |
| bounded exact-topic search over pinned mathlib and repo-local Lean | 0 | only mathlib's prose phrase "minimum distance" matched; no fixed-length block-code/minimum-distance/Singleton/MDS API or terminal code-bound theorem found; variable-length uniquely-decodable-code machinery is a different model; discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1587/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1587/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, source/duplicate boundaries, inventory, packet, hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1587/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1587` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1587 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The catalog does not choose the unrestricted q-ary, linear finite-field, puncturing, or MDS
  equality formulation.
- The exact primary bibliography is identified, but the paper text, theorem locator, assumptions,
  proof, corrections, errata, and independent H0 review are unavailable.
- The parallel Stage0-only `THM-C-0371` record uses a slightly more specific gloss; duplicate
  identity and ownership remain unresolved.
- Alphabet, code model, length, distance, dimension, puncturing, cardinal arithmetic, subtraction,
  powers, ranges, binder order, conclusion, and all degenerate cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
