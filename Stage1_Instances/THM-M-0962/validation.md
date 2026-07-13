# THM-M-0962 intake validation

## Boundary

This validates only `S56-M-0962-INTAKE`: target membership, the planned dossier, scope/source
crosswalk, open downstream DAG, and a discovery-only pinned-interface probe. It does not validate a
canonical Frankl-Wilson statement, source closure, a theorem body, obligation tree, proof, audit
completion, or theorem completion. The authoritative checklist and execution DAG remain `[ ]`;
`[_]` is only the worker proposal pending master acceptance.

Base repository revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`.
Base tree: `fdfff18dea4c6798c5b322b6088dfe556109c134`.
The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It targets canonical pinned artifacts, was used read-only, and
is excluded from this worker's changed paths. No `lake update`, `lake build`, dependency clone or
fetch, or other `.lake` mutation was run.

## Source discovery

On 2026-07-13, the publisher landing page and generated citation for DOI
`10.1007/BF02579457`, plus Crossref and OpenAlex metadata, were downloaded to temporary storage.
Their observed SHA-256 values are recorded in `instance.json`. The records agree on the Frankl and
Wilson 1981 article and expose its abstract. OpenAlex reports `is_oa=false`, no repository full
text, and one publisher location. A publisher PDF request returned HTML, so no paper body, theorem
locator, proof, or errata was inspected. These mutable network observations are source discovery,
not offline replay recipes or H0 evidence.

## Commands and results

All repository commands ran on 2026-07-13 in the isolated worker clone unless a cwd is shown.

| Cwd | Command | Exit | Result |
|---|---|---:|---|
| `.` | `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `.` | `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `.` | `python3 scripts/stage1_target.py show THM-M-0962` | 0 | rank 1496; planned; L0; no legacy slot; rework required; theorem incomplete |
| `.` | `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `.` | `git rev-parse HEAD HEAD^{tree}` | 0 | base revision/tree above |
| `.` | `curl` publisher landing, citation, Crossref, and OpenAlex endpoints into `/tmp`; `sha256sum`; structured metadata inspection | 0 | matching bibliographic identity and modular-bound abstract; article body unavailable; exact hashes in `instance.json` |
| `Formalizations/Lean` | `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`, x86_64 release |
| `Formalizations/Lean` | `lake --version` | 0 | Lake 5.0.0-src+98dc76e; no update or build run |
| `.` | `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib `8a178386...`; tree `bdc39a31...` |
| `.` | `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package source clean |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-0962/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `3efe1de6...14de`; stderr empty |
| `.` | `rg -ni 'frankl.?wilson|intersection theorems with geometric consequences' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no match in bounded pinned-mathlib source search; not an exhaustive anchor audit |
| `.` | `python3 -m json.tool` on structured artifacts; isolated `python3 -m py_compile` | 0 | JSON and scoped checker syntax pass |
| `.` | `python3 -B Stage1_Instances/THM-M-0962/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | final target/DAG/source/artifact/packet invariants pass |
| `.` | `python3 -B Stage1_Instances/THM-M-0962/check_intake.py` | 0 | public replay without scheduler packet passes |
| `.` | prohibited-construct scan over owned Lean files | 1 | expected no match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `.` | per-new-file `git diff --no-index --check /dev/null <file>` | 0 aggregate | every new owned artifact and worker packet has no whitespace diagnostic |
| `.` | `git diff --check -- Stage1_Instances/THM-M-0962 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

The Lean output was:

```text
Set.IsIntersectingOf.{u_1} {α : Type u_1} [DecidableEq α] (L : Set ℕ) (𝒜 : Set (Finset α)) : Prop
Set.Intersecting.{u_1} {α : Type u_1} [SemilatticeInf α] [OrderBot α] (s : Set α) : Prop
Set.Sized.{u_1} {α : Type u_1} (r : ℕ) (A : Set (Finset α)) : Prop
Finset.powersetCard.{u_1} {α : Type u_1} (n : ℕ) (s : Finset α) : Finset (Finset α)
Finset.card_powersetCard.{u_1} {α : Type u_1} (n : ℕ) (s : Finset α) :
  (Finset.powersetCard n s).card = s.card.choose n
Nat.ModEq (n a b : ℕ) : Prop
Nat.choose : ℕ → ℕ → ℕ
```

This authenticates only pinned vocabulary. It establishes no source-to-expression identity,
minimality of future target imports, theorem proof, provenance, or trust closure.

## Known failures

1. The primary article body was unavailable, so the exact theorem, definitions, assumptions,
   theorem/page locator, proof boundary, corrections, errata, and independent review remain open.
2. The catalog and abstract do not safely settle prime versus prime-power scope, listed-residue
   occurrence, residue carrier/order, exact distinct-pair condition, binomial typography, included
   equality/application claims, or degenerate cases.
3. Canonical Lean expression, minimal imports, expression/environment fingerprints, checked
   transports, and removed-hypothesis/domain/binder/boundary mutations remain open.
4. No Frankl-Wilson theorem declaration was located in the bounded pinned-mathlib search. External
   search, terminal-body/provenance/trust audit, and any implementation remain downstream work.
5. Obligation/discovery freezes, typed graphs, proof/composition, readable reconstruction, hermetic
   release evidence, independent validation, and master acceptance remain open.

The first retry condition is lawful access to and independent review of an exact primary theorem
body, followed by a complete source-to-statement mapping. No proof-tree construction is lawful
before that statement gate passes.

## Snapshot binding

The provisional receipt binds the final nonrelease worker snapshot with per-file SHA-256 values for
all nine owned artifacts plus the root worker packet. The receipt excludes itself from its own
digest to avoid self-reference. A canonical digest covers sorted
`<sha256>  <repo-relative-path>\n` records for every other changed path, and the receipt separately
binds the complete `git status --porcelain=v1 --untracked-files=all` output. This remains unsigned,
provisional worker evidence; the integration lane must recapture it for acceptance.
