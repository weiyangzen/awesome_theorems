# Intake validation

## Boundary

This validates only the `S56-M-0934-INTAKE` planned dossier, scope/source crosswalk, open downstream
DAG, and discovery-only pinned API probe. It does not validate a canonical Erdos-Heilbronn
statement, H0 source closure, formal candidate, proof-body provenance, obligation tree, proof,
audit completion, or theorem completion. The authoritative execution item remains `[ ]`; the root
worker packet proposes only `[_]` pending integration-lane review.

Base repository revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`.
Base tree: `018557070da18ea1733a82de81a238750c59aa84`.
Initial worktree status contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It points to the canonical pinned artifacts, was used read-only,
and is excluded from this worker's changed paths. No `lake update`, `lake build`, dependency clone,
fetch, or `.lake` mutation was run.

## Commands and results

All commands ran on 2026-07-13 in the isolated worker clone unless another cwd is shown.

| Cwd | Command | Exit | Result |
|---|---|---:|---|
| `.` | `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `.` | `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `.` | `python3 scripts/stage1_target.py show THM-M-0934` | 0 | rank 1473; planned; L0; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `.` | `git status --short --untracked-files=all` | 0 | pre-edit output only `?? Formalizations/Lean/.lake` |
| `.` | `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `.` | immutable download and inspection of `https://arxiv.org/pdf/1210.6509v2` | 0 | 198290-byte survey PDF; SHA-256 `fb3e54b...5b26c`; PDF page 3 distinguishes two-set, `A = B`, and 1964-paper boundaries |
| `.` | normalized Crossref API inspection for DOIs `10.4064/aa-9-2-149-159` and `10.1112/blms/26.2.140` | 0 | bibliographic identities confirmed; normalized SHA-256 values `9dea8d3b...ecd5` and `46c0315b...996f` |
| `Formalizations/Lean` | `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`, x86_64 release |
| `Formalizations/Lean` | `lake --version` | 0 | Lake 5.0.0-src+98dc76e |
| `.` | `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib `8a178386...`; tree `bdc39a31...` |
| `.` | `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package source clean |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-0934/IntakeProbe.lean` | 0 | eight adjacent interfaces elaborated; `ZMod.cauchy_davenport` axioms `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `bc7531f3...f2f3` |
| `.` | exact-topic `rg` search of repository Lean and pinned mathlib | 1 (expected no match) | no obvious Erdos-Heilbronn, Dias da Silva, or restricted-sumset declaration; bounded intake discovery only |
| `.` | `python3 -B Stage1_Instances/THM-M-0934/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target, DAG, source, artifact, and worker-packet invariants pass |
| `.` | scoped prohibited-construct scan of owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `.` | scoped per-file no-index whitespace checks and `git diff --check` | 0/1 | expected new-file differences only; no whitespace diagnostics |

`check_intake.py` also passed without the scheduler packet, so the public dossier can replay its
own invariants. `intake-receipt.json` records exact output and artifact hashes for this provisional
nonrelease snapshot; the receipt excludes itself from its own digest to avoid self-reference.

## Known failures

1. The exact root is not selected among all-subset sums, restricted `A = B` pair sums, the later
   two-set restricted theorem, and the `h`-fold Dias da Silva-Hamidoune family.
2. No independently approved primary statement/proof packet maps all domains, binders, premises,
   definitions, small-cardinality cases, corrections, errata, and the `THM-M-0935` ownership split.
3. Canonical Lean expression, minimal imports, expression/environment fingerprints, alternate
   transports, and removed-hypothesis/domain/binder/boundary mutation tests remain open.
4. No exact formal candidate is credited. Pinned `Finset.subsetSum` is a different construction,
   and `ZMod.cauchy_davenport` is unrestricted. Full anchor/provenance/trust discovery is downstream.
5. Obligation registry, typed graphs, proof, composition, readable reconstruction, hermetic replay,
   deterministic evidence, independent verification, release, and master acceptance remain open.

The first retry condition is an independently reviewed exact primary source selection and complete
source-to-statement map. No proof-tree construction is lawful before that statement gate passes.
