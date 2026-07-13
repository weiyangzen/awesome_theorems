# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`; base tree:
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`.

Commands were run from the repository root on 2026-07-13 (Asia/Shanghai). The automation-provided
`Formalizations/Lean/.lake` symlink was present before the work and was used read-only. No `lake
update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. This dirty worker snapshot is nonrelease evidence.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof because the catalog does not supply a
truth-valued linear-code proposition.

## Source boundary

Venkatesan Guruswami's *Introduction to Coding Theory*, CMU Spring 2010, Notes 1, was downloaded
to temporary worker storage and inspected. The 11-page, 167041-byte PDF has SHA-256
`9948552eeea3d451644cb0c5196a18f391ab197c0c23cd06b476e0350b1d0df8`. Printed pages 5-9
separate the linear-code definition, generator representation, systematic form, parity-check
kernel, distance and duality claims. This supports family discrimination only. The catalog cites
no source and selects none of those claims; the temporary PDF is not a repository artifact and no
H0 source admission, complete errata review, or independent review is claimed.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1589` | 0 | rank 1210; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `Formalizations/Lean/.lake` was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 11707,11712 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| download and `pdftotext -layout` inspection of the Guruswami notes in temporary storage | 0 | recorded Definition 7, Definition 8, Exercises 1-4, Lemma 9, and Definition 15 as distinct uncredited source surfaces |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| bounded `rg` for linear-code terms in pinned mathlib and repo-local Lean | 0 only for generic Hamming prose | no exact `LinearCode` abstraction or terminal theorem located under recorded terms; discovery only, not an exhaustive anchor audit |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1589/IntakeProbe.lean` | 0 | eight Hamming, submodule, and matrix API signatures elaborated; complete stdout SHA-256 `4856b69bb534b413bd33b04f71e6bf23e0b1e2596f28ccc4ffd6700183c79492` |
| `python3 -m json.tool` on every structured owned artifact and `.stage1-worker-selftest.json` | 0 | all final structured artifacts parsed as JSON |
| Python `ast.parse` on `Stage1_Instances/THM-M-1589/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1589/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, null target, source and neighbor boundaries, exact inventory, packet, pins, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1589/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 (expected no match) | the discovery-only probe contains no prohibited declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index difference is only the expected new file |
| `git diff --check -- Stage1_Instances/THM-M-1589 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; preceding no-index checks cover untracked files |

## Known downstream failures

- The catalog code-class title and gloss do not select one truth-valued proposition. An accountable
  correction or independently reviewed immutable source decision is required.
- Field, word/code representation, matrix orientation, dimension, cardinality, distance, duality,
  encoder/decoder, binder order, exact conclusion, and every boundary case remain open.
- No canonical Lean expression, exact minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor and proof-body audit, discovery protocol, obligation registry, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
