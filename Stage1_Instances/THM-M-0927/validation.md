# Intake validation

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d`; base tree:
`0d6c1fdf06d1573c256af331c6b198e5a787af43`. Validation date: 2026-07-13
(Asia/Shanghai).

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The new
target-owned dossier and root worker packet make this nonrelease dirty worker evidence.

Validation covers target-set consistency, planned dossier structure and source/scope invariants,
repository provenance, the six-task open DAG, a narrow pinned Lean Binet-interface and axiom probe,
prohibited-construct hygiene, JSON syntax, and whitespace. It does not validate a canonical
statement, historical source fidelity, terminal proof provenance, an exhaustive anchor inventory,
audit completion, theorem completion, or master acceptance.

## Source boundary

The repository supplies only the uncited record at `Docs/researches/math_theorems.md:6777-6782`;
all six lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Stage0 repeats
the explicit-formula gloss while leaving the exact definition, premises, proof, foundation,
axioms, and artifacts open.

NIST DLMF section 26.11 was inspected. Equations 26.11.5 and 26.11.7 give a zero-based Fibonacci
definition and the nonnegative-index radical formula. The replayable equation-TeX hashes are
recorded in `instance.json` and `source-statement-crosswalk.md`. This is a pinpoint modern
statement lead, not a primary Binet 1843 proof source or accepted H0 crosswalk. OEIS A000045 and
MathWorld were bounded secondary leads only; request-varying live HTML is not a replayable input.
No primary historical edition, proof, translation, correction/errata audit, or independent review
was admitted. Human status remains H1.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `Mathlib/NumberTheory/Real/GoldenRatio.lean` SHA-256:
  `e3a6e5160e654dfb4c5594c66a624fa7a5edffa4c1b839d992be7d1ba2dd7ac3`.
- Pinned `Mathlib/Data/Nat/Fib/Basic.lean` SHA-256:
  `cc677908e449079923644aed447699e331e0100c88597d8a3c6e491db98267a0`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0927` | exit 0; rank 1546, planned, L0/rework_required, no accepted legacy artifacts, theorem_complete false |
| initial `git status --short --untracked-files=all` | exit 0; only the pre-existing automation `.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree shown above |
| `git blame -L 6777,6782 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded DLMF 26.11, OEIS A000045, MathWorld, Crossref, OpenAlex, and Archive.org queries | mixed; DLMF/OEIS/MathWorld/Crossref responses were inspected and hashed; OpenAlex returned HTTP 429 and Archive.org timed out; no failed request supplied evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean version and commit recorded above; no update or build ran |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake version recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1 --untracked-files=all` | exit 0 with empty output; pinned package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0927/IntakeProbe.lean)` | exit 0; six Fibonacci/root/Binet interfaces elaborated; three axiom reports were `[propext, Classical.choice, Quot.sound]`; complete output was 609 bytes, SHA-256 `b2c14775013bf6ba8eb73815a507779c04caabae8b6070e5747deb5302bb05f2` |
| `python3 -m json.tool` on all owned JSON files and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0927-pycache python3 -m py_compile Stage1_Instances/THM-M-0927/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0927/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, source and pin hashes, null canonical target, H1/M3/R4 boundary, inventory, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0927/check_intake.py` | exit 0; public replay mode passes without the scheduler-only root packet |
| prohibited Lean declaration scan over `Stage1_Instances/THM-M-0927` | exit 1 as expected for no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and per-new-file whitespace checks | exit 0/no diagnostics after finalization; all owned files and worker packet have final newlines, LF endings, and no trailing whitespace |

## Known open gates

An independently accepted immutable primary or authoritative edition, exact formula and proof
locators, definitions, attribution history, corrections, errata, and source review remain open. So
do selection of natural or integer indices, indexing and codomain, characteristic-root and
square-root conventions, power and denominator spelling, equality form, ordered binders, checked
transports, canonical Lean expression and environment fingerprint, minimal import certificate, all
four mutation classes, exhaustive anchor and terminal-body audit, obligation and discovery freezes,
typed graphs, proof and composition acceptance, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, release, and master acceptance.

These failures prevent downstream statement, audit, and theorem completion. They do not invalidate
the self-tested `planned` intake, whose only proposed scheduler state is provisional `[_]` pending
master integration.
