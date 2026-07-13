# Intake validation

Base revision: `5bc32428da3d17f138ceca67f30fbc2d149da1ba` (tree
`7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target membership, the planned dossier and source/scope boundaries, the
six-node open task DAG, current authority and dependency hashes, a narrow pinned Lean discovery
probe, proof-escape hygiene, JSON integrity, and whitespace. It does not validate a canonical
Tychonoff statement or proof because the exact source formulation and encoding are not frozen.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

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
- Pinned compactness module SHA-256:
  `b98c88119c35b7f0a0b8ab922d4f8c63cb2074c3326dbdf58cf1b838b77faf18`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0620` | 0 | rank 1314, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 4601,4606 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI query, publisher availability check, and Goettingen IIIF/OCR inspection | 0 | Tychonoff 1930 bibliography located; IIIF manifest SHA-256 `66ba71aa...ec10`; printed pp. 544-561 inspected; Section 2 from p. 548 proves compactness of an arbitrary interval power, but no clean exact general compact-space product source row was identified |
| permanent Encyclopedia of Mathematics revision inspection | 0 | conventional general statement located in `oldid=38785`; observed HTML SHA-256 `a1056109...0cbd`; secondary formulation lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded above; empty package status |
| bounded `rg` and source inspection for Tychonoff, Pi topology, compact products, compactness definitions, and fixed-point neighbors | 0 | three direct pinned compact-product candidates found; Pi product topology and non-Hausdorff compactness convention identified; fixed-point targets excluded |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0620/IntakeProbe.lean)` | 0 | three direct candidates, `isCompact_empty`, three representative boundary instances, and a generic dependent-product instance elaborated; all three candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `883ca17e...f065` |
| `python3 -m json.tool` on owned JSON and the root worker packet | 0 | all finalized structured artifacts parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0620-pycache python3 -m py_compile Stage1_Instances/THM-M-0620/check_intake.py` | 0 | intake validator compiles without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0620/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, hashes, planned H1/M3/R4 null-target boundary, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0620/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 | expected no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file no-index whitespace checks plus scoped `git diff --check` | 0 | no whitespace diagnostics |

## Known open gates

An independently reviewed exact primary theorem for the received general formulation; exact
source genealogy, historical terminology and definitions, assumptions, corrections and errata;
the space-level versus compact-subset root;
product-topology and compactness/separation conventions; universes and ordered binders; empty-index,
empty-factor and non-Hausdorff boundaries; and the accepted classical-choice profile remain open.
So do canonical target elaboration and mutations, exhaustive anchor/provenance/trust audits,
discovery and obligation freezes, typed graphs, proof and composition, source-faithful readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, master
acceptance, audit completion, and theorem completion.

These open gates do not invalidate a truthful self-tested `planned` intake. Only the integration
lane may accept the provisional worker receipt.
