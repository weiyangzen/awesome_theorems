# Intake validation

## Validation boundary

This record validates a fail-closed `planned` intake, not an exact theorem statement or proof. It
checks target membership, structured scope, source-candidate discrimination, the six-node open
task DAG, pinned exact-topic Lean interfaces, artifact hygiene, and the provisional worker handoff.

The canonical statement, formal target, expression fingerprint, checked transports, obligation
registry, proof body, composition, trust closure, readable proof, hermetic replay, independent
verification, and release remain open.

## Source inspection

The complete GDZ scan of Adolf Hurwitz, *Über die Fourierschen Konstanten integrierbarer
Funktionen*, *Mathematische Annalen* 57 (1903), 425-446, DOI `10.1007/BF01445179`, was retrieved
temporarily and inspected page by page. Its SHA-256 was
`014ca3260c37902f51daf64fa12588af618e7ae709c8c75f09042c6b038fbebb`. The accompanying IIIF
manifest SHA-256 was `9d63f613369d1338dfa8c1d658e37fd392e2c4772456d1a87f418be72378fe4c`.

The scan identifies several non-equivalent possible roots. The intake crosswalk records the
absolute coefficient-product statement on page 436, the absolutely convergent indefinite-integral
expansion on pages 438-440, and the distinct Sturm-Hurwitz theorem on pages 442-446. The source was
not added to the repository. The scan and Crossref metadata are discovery evidence only; no H0
source admission or independent translation review is claimed.

## Lean environment and result

The probe used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone/fetch, or other dependency mutation was run.

`IntakeProbe.lean` elaborated eight adjacent APIs, a type-correct historical-period specialization,
and two axiom reports. Its complete stdout was 15 lines and 1427 bytes with SHA-256
`e803388b7b79edd4efc8bb2cdbcfc9a5489cdb8c5584c74b63b2ae4afc2a0478`; stderr was empty with
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Both inspected mathlib theorems report only `propext`, `Classical.choice`, and `Quot.sound`.

The probe deliberately proves no Hurwitz theorem. In particular,
`hasSum_fourier_series_of_summable` consumes `Summable (fourierCoeff f)`; it does not supply the
missing source-specific implication into summability.

## Commands and exact results

Commands ran from the isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0293` | 0 | rank 1543; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD HEAD^{tree}` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision `72e9e8092182121a6794921f61fcc9cae22f726d`, tree `0d6c1fdf06d1573c256af331c6b198e5a787af43` |
| Crossref DOI query and complete GDZ article/IIIF retrieval and page inspection | 0 | author/year/title/pages matched; hashes recorded above; source candidate branches discriminated; discovery/H1 only |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0293/IntakeProbe.lean` | 0 | eight interfaces plus a period specialization elaborated; two axiom reports printed; no target theorem declared |
| JSON parsing, Python AST parsing, scoped invariant checker, prohibited-token scan, and whitespace checks | 0 or expected no-match 1 | all planned-intake invariants and hygiene gates passed; details are bound in `intake-receipt.json` |

The final checker command and exact digest checks are replayed after the provisional receipt and
root worker packet exist. The receipt records their final exit status and hashes.

## Status boundary

This is self-tested provisional worker evidence for `S56-M-0293-INTAKE`. It supports only a
`planned` dossier with `[H1, M3, R4]` and six open downstream tasks. It does not support exact
statement elaboration, proof credit, audit completion, theorem completion, content-addressed
acceptance, or master acceptance.
