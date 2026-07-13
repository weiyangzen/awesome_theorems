# Intake validation

Base revision: `3ef3a6bf4f2f9b86930beb27693f7429fea3e63a`; base tree:
`c9eba4c65f6e228f9cefc8bdf62136b7fb69426a`.

This validation covers target membership, the planned dossier and open task DAG, catalog and source
provenance, JSON and scoped invariants, a narrow pinned Lean substrate probe, a bounded repo-local
and mathlib search, prohibited-construct hygiene, and whitespace. It does not validate a canonical
theorem statement or proof because the exact source-approved Lean encoding belongs to the downstream
statement phase and remains open.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref and Elsevier metadata identify W. T. Tutte, *A theory of 3-connected graphs*,
Indagationes Mathematicae (Proceedings) 64 (1961), 441-455, DOI
`10.1016/S1385-7258(61)50045-5`, PII `S1385725861500455`. The metadata endpoints did not provide
the article body, and the publisher PDF route returned an access-denial page. Thus primary
bibliographic identity is recorded, but no exact original theorem locator or source mapping is
claimed.

The versioned arXiv PDF for Carmesin and Kurkofka, *Canonical Decompositions of 3-Connected
Graphs*, `2304.00945v3`, was inspected. Section 2.7, page 56 defines minimal 3-connectivity using
both deletion and contraction of every edge and states Theorem 2.7.1: every minimally 3-connected
finite graph is a wheel. The PDF SHA-256 is
`6856032350da337d118b9954cdcecd0558685e2af57f10d78eb262fa30cbbadd`. This precise source
disambiguates a likely theorem core but does not choose the catalog's broader "wheel decomposition"
root or supply H0 review.

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

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0864` | 0 | rank 1418; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6334,6339 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query and DOI/Unixref retrieval for the primary title/DOI | 0 | author, title, year, journal, volume, pages, DOI, PII, and metadata links confirmed; no primary theorem-text credit |
| Elsevier metadata request | 0 | bibliographic core returned without article body; no exact original statement or H0 credit |
| versioned arXiv metadata/PDF retrieval plus `pdfinfo` and `pdftotext` | 0 | `2304.00945v3`, Section 2.7 and Theorem 2.7.1 inspected; PDF and text hashes recorded in `instance.json` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0864/IntakeProbe.lean)` | 0 | eight adjacent connectivity, deletion, cycle, isomorphism, and operation APIs elaborated; complete output SHA-256 `3d6040d1564a9ea4fc42594ec8e9ca555a38d4122be45de05f15b28dacf94fcb`; no target declaration |
| exact-topic `rg` search over pinned mathlib and repo-local Lean | 1 (expected no exact target match) | no Tutte wheel theorem, ordinary wheel predicate, vertex 3-connectivity predicate, or edge-contraction definition; unrelated matching and wheel-like names explicitly excluded |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python compile of `Stage1_Instances/THM-M-0864/check_intake.py` | 0 | scoped validator parses without writing bytecode into the owned path |
| `python3 -B Stage1_Instances/THM-M-0864/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null target, source and dependency pins, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0864/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the API probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file no-index whitespace checks plus `git diff --check` | 0 aggregate | no whitespace diagnostics |

## Known downstream failures

- The primary article is bibliographically identified but its exact theorem, definitions, proof,
  corrections, and independent source review remain open.
- The catalog does not select the minimal characterization or a reduction/construction sequence.
- Exact graph carriers, vertex 3-connectivity, wheel, deletion, contraction, simplification,
  operation sequence, ordered binders, and boundary cases are not frozen as one proposition.
- No canonical Lean expression, minimal-import certificate, expression/environment fingerprint,
  checked alternate encoding, or required statement mutation exists.
- Exhaustive formal anchor audit, discovery and obligation freezes, typed graphs, proof,
  composition, readable reconstruction, trust closure, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the known scope and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
