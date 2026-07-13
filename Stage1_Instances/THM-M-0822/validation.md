# Intake validation

## Boundary

This validates only the `S56-M-0822-INTAKE` planned dossier, source/scope crosswalk, open downstream
DAG, and discovery-only pinned candidate probe. It does not validate a canonical EKR statement,
source closure, proof-body provenance, obligation tree, proof, audit completion, or theorem
completion. The authoritative checklist and execution DAG remain `[ ]`; `[_]` is only the worker
handoff proposal pending master acceptance.

Base repository revision: `902d9ce008e88a35a2307c85355560a230cc33c2`.
Base tree: `dfc20d8141f18f6b09a03e818acfff408e836714`.
Initial worktree status contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It targets the canonical pinned artifacts, was used read-only,
and is excluded from this worker's changed paths. No `lake update`, `lake build`, clone, fetch, or
dependency mutation was run.

## Commands and results

All commands ran on 2026-07-13 in the isolated worker clone unless another cwd is shown.

| Cwd | Command | Exit | Result |
|---|---|---:|---|
| `.` | `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `.` | `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `.` | `python3 scripts/stage1_target.py show THM-M-0822` | 0 | rank 1380; planned; L0; no legacy slot; rework required; theorem incomplete |
| `.` | `git status --short --untracked-files=all` | 0 | pre-edit output only `?? Formalizations/Lean/.lake` |
| `.` | `git rev-parse HEAD HEAD^{tree}` | 0 | base revision/tree above |
| `.` | bounded range download of `https://www.renyi.hu/~p_erdos/1961-07.pdf` to `/tmp/ekr-original.pdf` | 0 | complete 1,292,421-byte, eight-page primary scan |
| `.` | `sha256sum /tmp/ekr-original.pdf` | 0 | `e53f1ec72accc8e55ec8da360588b224542a9133216d4b82a6918bbe309ac821` |
| `.` | `pdftotext -layout /tmp/ekr-original.pdf /tmp/ekr-original.txt` plus rendered-page inspection | 0 | printed pp. 313-316 mapped; antichain premise visually confirmed |
| `Formalizations/Lean` | `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`, x86_64 release |
| `Formalizations/Lean` | `lake --version` | 0 | Lake 5.0.0-src+98dc76e |
| `.` | `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib `8a178386...`; tree `bdc39a31...` |
| `.` | `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package source clean |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-0822/IntakeProbe.lean` | 0 | candidate and six APIs elaborated; axioms `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `d83eb287...9f21`, stderr empty |
| `.` | `python3 -B Stage1_Instances/THM-M-0822/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG/source/artifact/packet invariants pass |
| `.` | `python3 -B Stage1_Instances/THM-M-0822/check_intake.py` | 0 | public replay without scheduler packet passes |
| `.` | `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0822` | 1 | expected no match; no prohibited declaration |
| `.` | per-file `git diff --no-index --check /dev/null <new-file>` | 0/1 | expected new-file difference only; no whitespace diagnostics |
| `.` | `git diff --check -- Stage1_Instances/THM-M-0822 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

The Lean stdout was:

```text
Finset.erdos_ko_rado {n : ℕ} {𝒜 : Finset (Finset (Fin n))} {r : ℕ} (h𝒜 : (↑𝒜).Intersecting) (h₂ : Set.Sized r ↑𝒜)
  (h₃ : r ≤ n / 2) : 𝒜.card ≤ (n - 1).choose (r - 1)
Set.Intersecting.{u_1} {α : Type u_1} [SemilatticeInf α] [OrderBot α] (s : Set α) : Prop
Set.Sized.{u_1} {α : Type u_1} (r : ℕ) (A : Set (Finset α)) : Prop
Finset.powersetCard.{u_1} {α : Type u_1} (n : ℕ) (s : Finset α) : Finset (Finset α)
Finset.card_powersetCard.{u_1} {α : Type u_1} (n : ℕ) (s : Finset α) : (Finset.powersetCard n s).card = s.card.choose n
Nat.choose : ℕ → ℕ → ℕ
'Finset.erdos_ko_rado' depends on axioms: [propext, Classical.choice, Quot.sound]
```

This authenticates only the displayed pinned candidate and vocabulary. It does not show identity
with the unfrozen repository root, minimality of imports, accepted provenance/trust closure, or an
attainment/equality theorem.

## Known failures

1. Exact root selection among original antichain/at-most-size Theorem 1, uniform upper bound, sharp
   maximum, and equality characterization remains open.
2. Systematic errata/corrections disposition and independent source review remain open; H0 is not
   claimed. The inspected secondary equality formulation overstates uniqueness at `n = 2r` and is
   not admitted to resolve the boundary.
3. Canonical Lean expression, minimal imports, expression/environment fingerprints, checked
   transports, and removed-hypothesis/domain/binder/boundary mutation tests remain open.
4. The pinned candidate's terminal body, transitive dependencies, placeholder/unsafe/oracle state,
   trust profile, and exact-root eligibility require the downstream anchor audit; M0 is not claimed.
5. Obligation/discovery freezes, typed graphs, proof/composition, readable reconstruction, hermetic
   and independent validation, deterministic release evidence, and master acceptance remain open.

The first retry condition is a reviewed exact statement selection and complete source-to-statement
mapping. No downstream proof-tree construction is lawful before that statement gate passes.

## Snapshot binding

The provisional receipt binds the final nonrelease worker snapshot with per-file SHA-256 values for
all nine owned artifacts plus the root worker packet. The receipt itself is explicitly excluded from
its own digest to avoid self-reference. A canonical digest covers sorted
`<sha256>  <repo-relative-path>\n` records for every other changed path, and the receipt separately
binds the complete `git status --porcelain=v1 --untracked-files=all` output. It also records stdout
and stderr hashes for both structured recipes, both checker modes, the prohibited-construct scan,
the whitespace checks, and the pinned mathlib status check. `check_intake.py` recomputes the local
artifact, packet, status, and expected-output bindings; external primary-source hashes remain
provisional claims for the integration lane to recapture.
