# Anchor audit

## Audit boundary

This audit is for `S56-M-0391-ANCHOR_AUDIT`. It searches for a terminal Lean 4
proof of the exact `Nat` proposition `Stage1Instances.THMM0391.MihailescuTarget`.
It does not credit similarly named combinatorics, polynomial analogues,
statement-only declarations, conditional wrappers, or finite special cases.

The repository snapshot is `1a43068b1644e78dd234d738040b40e4dea60bcb`.
The local Lake manifest pins mathlib4 to
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and `flt-regular` to
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; both checked-out dependency HEADs
match those immutable revisions. No dependency was fetched or changed.

## Candidate ledger

| Candidate | Immutable revision | Exact module / declaration | Audit result | Integration decision |
|---|---|---|---|---|
| mathlib documentation entry | `leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95` | `docs/1000.yaml`, `Q174955` | Title is `Mihăilescu's theorem`, but the row has no `decl` or `decls`; it is a documentation wish-list entry, not a theorem. | Reject as machine anchor. |
| mathlib polynomial Fermat-Catalan theorem | same mathlib revision | `Mathlib.NumberTheory.FLT.Polynomial`, `Polynomial.flt_catalan` | Its checked-in source type has polynomials over a field and concludes that three polynomial degrees are zero. It neither accepts nor concludes the frozen natural-number equation/tuple. The canonical reused `.lake` has no `Mathlib.olean`, so a narrow import check is unavailable without mutating dependencies. | Keep only as adjacent proof infrastructure; no wrapper can close the root from it. |
| mathlib Catalan modules | same mathlib revision | `Mathlib.Combinatorics.Enumerative.Catalan`; `Mathlib.RingTheory.PowerSeries.Catalan` | Name collisions concerning Catalan numbers and their generating series. | Reject as theorem candidates. |
| flt-regular | `leanprover-community/flt-regular@56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` | complete checked-out Lean/Markdown tree | Searches for `Mihailescu`, `Mihăilescu`, `Catalan's conjecture`, `consecutive perfect power`, and `PerfectPower` returned no candidate. | No terminal anchor and nothing to integrate. |
| Formal Conjectures | `google-deepmind/formal-conjectures@7871d8fc7a8164a1ac16c3765b40c25ce015b681` | `FormalConjectures/Wikipedia/Catalan.lean`, `Catalan.catalans_conjecture` | Close statement surface, but the body is literally `by sorry`. It also uses truncated `Nat` subtraction and assumes only positive bases. Toolchain is Lean `v4.27.0`; mathlib input is `v4.27.0`. | Reject as proof evidence. Do not add a dependency: it provides no terminal proof body. |

The external file and its project metadata were read from commit-qualified raw
GitHub URLs. The fetched `Catalan.lean`, `lean-toolchain`, and `lakefile.toml`
bytes had SHA-256 digests
`4d6a944a1cec1df6928207be2cdf44ad0b1e7bdc89263f9812fc93037f6b152c`,
`e695e6e5d8e7a8be4d6cf159dfb995847993d26c6cc450353a86f387279025b9`, and
`5d457870495adcd8bd1eaf678d1673e7b24939280e13c6b2cfc29e1f76437659`,
respectively. These hashes make the inspected external evidence content-addressed;
the project was not cloned into `.lake`.

## Search and validation evidence

Run from the repository root:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0391
  exit 0: execution rank 5; planned; theorem_complete=false
git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95
git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD
  exit 0: 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27
rg -n -i 'mihailescu|mihăilescu|catalan.?s conjecture|consecutive perfect power|perfectpower' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib \
  Formalizations/Lean/.lake/packages/mathlib/docs \
  Formalizations/Lean/.lake/packages/flt-regular -g '*.lean' -g '*.md' -g '*.yaml'
  exit 0: only mathlib docs Q174955 and Polynomial.flt_catalan matched; no flt-regular match
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0391/Statement.lean
  exit 0: exact statement and its statement-only checks elaborated
```

A probe importing `Mathlib.NumberTheory.FLT.Polynomial` failed because the
canonical reused dependency cache has no `Mathlib.olean` module root. Per the
worker rules, this audit did not run `lake build`, update, clone, or fetch to
repair that cache. This is a known validation limitation, not evidence against
the source-level type mismatch and not a blocker to the negative anchor
inventory.

The three external hashes were produced by piping the three immutable raw URLs
to `sha256sum`; all requests exited 0. `python3 -m json.tool` was also run on
`instance.json`, and `git diff --check` was run on the owned changes; both exited
0.

## Verdict and debt boundary

The candidate inventory is complete for the pinned local dependency closure and
the identified credible external Lean 4 project. No candidate supplies a proof
body for the exact root. Therefore the anchor-audit phase is self-tested, but
the theorem remains `[H1, M4, R4]`, `audit_complete=false`, and
`theorem_complete=false`. There is no actionable `repo_local_integration_debt`:
the sole close external declaration is a placeholder, so importing it would not
improve machine assurance. The remaining root cut set begins with a genuine
formal proof (or a future immutable external proof) and the later obligation,
validation, and release gates.
