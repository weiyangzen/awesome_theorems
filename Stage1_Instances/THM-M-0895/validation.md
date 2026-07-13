# Intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d`; base tree:
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, source and non-substitution boundaries, JSON and scoped invariants, a narrow pinned
Lean strongly regular graph API probe, prohibited-construct hygiene, and whitespace. It does not
validate a canonical theorem statement or proof because the source gloss does not select one
parameter constraint.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

The uncited catalog record was traced to its introduction commit. Publisher and Crossref metadata
identify the exact 1963 Bose paper *Strongly regular graphs, partial geometries and partially
balanced designs*, Pacific Journal of Mathematics 13(2), 389-419, DOI
`10.2140/pjm.1963.13.389`. A complete 3,289,073-byte, 35-page publisher PDF was inspected from
temporary storage (SHA-256 `2d73e396...be614`). Section 2, printed pages 393-395, states that the
graph parameters obey equations (2.1)-(2.5); later sections give distinct partial-geometry and
integrality constraints. The catalog does not select among these. Intake did not admit an exact
root, complete source mapping, corrections or errata decision, or independent review. The source
classification therefore remains H1 rather than H0.

## Environment fingerprint

- Platform: Linux `7.0.0-27-generic`, x86_64, Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `Mathlib/Combinatorics/SimpleGraph/StronglyRegular.lean` SHA-256:
  `23476d5bc0a98578f9e676c835782f67fb10ec0f8a24f2b7599c9f3cfb70f6ab`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0895` | 0 | rank 1444; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6551,6556 -- Docs/researches/math_theorems.md` | 0 | all six uncited source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| read-only Crossref, publisher page, and complete PDF inspection for DOI `10.2140/pjm.1963.13.389` | 0 | exact Bose 1963 match; complete PDF size 3,289,073 bytes, 35 pages, SHA-256 `2d73e396...be614`; Section 2 equations (2.1)-(2.5) and later distinct constraints confirm ambiguity; H1 only |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 | pinned module contains `IsSRGWith`, `param_eq`, `matrix_eq`, and `compl`; no repo-local source-approved THM-M-0895 target exists |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0895/IntakeProbe.lean)` | 0 | ten adjacent pinned interfaces elaborated; complete output SHA-256 `94e1c153b7c72776755d12346ffa6af6402b085cef84450356f5a15262bb68df` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0895/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0895/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M3/R4 boundary, null target, inventory, source hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0895/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0895 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- No independently approved immutable primary text, pinpoint proposition, definition and
  assumption map, complete proof boundary, correction or errata audit, or H0 review exists.
- The catalog does not choose among the elementary feasibility equation, matrix identity,
  complement formula, spectral restrictions, multiplicity integrality, feasibility bounds,
  geometry/design relations, or a conjunction. Nontriviality, positivity, parameter order,
  arithmetic domain, binders, and degenerate cases remain open.
- No canonical Lean expression, exact minimal imports, expression or environment fingerprint,
  checked alternate encoding, or statement mutation is frozen. Close pinned declarations support
  only the provisional M3 interface classification, not M0 proof credit.
- Formal anchor and provenance audit, discovery and obligation freezes, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
