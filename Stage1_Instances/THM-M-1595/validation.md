# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`; base tree:
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, primary-source theorem-family discrimination, duplicate and neighbor boundaries, JSON
and scoped invariants, a narrow pinned Lean substrate probe, bounded exact-topic search,
prohibited-construct hygiene, and whitespace. It does not validate a canonical polar-code theorem
or proof because the catalog does not select one exact proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The author-posted `arXiv:0807.3917v5` version of Arikan's 2009 paper was downloaded to temporary
worker storage and inspected. The 23-page, 545,830-byte PDF has SHA-256
`36046a14f967b7b8be88a9e7beb4dd1de475a1d689b97dc43a05a3279e1c2f4d`; its layout-text extract
has SHA-256 `9339998e57f042c20c29b6a7b494ba25e88cdc2113fa33b49216e1c8b1163d8d`.
Section I, Theorems 1 through 5, was inspected to distinguish polarization, good-channel,
block-error, frozen-vector, symmetry, and complexity claims.

The source supports family discrimination and provisional H1 only. The catalog does not cite or
select a theorem, no source file was added to the repository, and no accepted archive, canonical
transcription, complete correction/errata and premise mapping, or independent H0 review is claimed.

## Environment fingerprint

- Platform: Linux x86_64, kernel `7.0.0-27-generic`.
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
| `python3 scripts/stage1_target.py show THM-M-1595` | 0 | rank 1215; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 11749,11754 -- Docs/researches/math_theorems.md` | 0 | all six uncited mathematical catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --retry 2 --fail --silent --show-error --max-time 120 -o <temporary-PDF> https://arxiv.org/pdf/0807.3917v5` | 0 | retrieved the 23-page source lead with the PDF digest above; no source bytes added to the repository |
| `pdftotext -layout <temporary-PDF> <temporary-text>` and bounded inspection | 0 | extracted text with the digest above; inspected Theorems 1-5 and their distinguishing definitions |
| Crossref request for DOI `10.1109/TIT.2009.2021379` | 0 | confirmed title, author, July 2009, journal, volume 55(7), and pages 3051-3073; response SHA-256 `6e9771d58437d578d6b22e3ef24712938bba9741d438fb369897302538088773` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1595/IntakeProbe.lean)` | 0 | ten adjacent probability, kernel, entropy, Hamming, and matrix APIs elaborated; complete output SHA-256 `bf36075a82086b7a090af1854ad7164578d486a0b38e576896b5ef4bb22300db` |
| bounded exact-topic search over pinned mathlib and repo-local Lean | 0 | only an unrelated author surname and an unrelated metadata URL matched; no polar-code, channel-polarization, mutual-information, or capacity declaration found; discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1595/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1595/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, source/duplicate boundaries, inventory, packet, hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1595/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-declaration scan over owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1595 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The catalog does not select Arikan Theorem 1, 2, 3, 4, 5, or an exact approved composition.
- "Shannon limit" does not resolve general B-DMC symmetric capacity versus Shannon capacity for
  the symmetric subclass, nor averaged versus fixed frozen vectors.
- The inspected author-posted version has not been independently admitted to H0 with a complete
  journal/version, correction, incorporated-definition, premise, proof-boundary, and errata review.
- `THM-C-0386` repeats the family outside Stage1; duplicate identity and ownership remain open.
- Channel, capacity, transform, information and frozen sets, decoder, error, rate, block length,
  asymptotic quantifiers, big-O meaning, complexity boundary, and all degenerate cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
