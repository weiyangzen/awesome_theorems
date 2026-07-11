# Anchor audit record

Item: `S56-M-0002-ANCHOR_AUDIT`  
Base revision: `7f2287693d2d333c6cc744c9bdd80267232cdc12`  
Audit date: 2026-07-12

## Decision

The immutable mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains an exact
candidate in `Mathlib.CategoryTheory.Abelian.DiagramLemmas.Four`:
`CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono`. After introducing the frozen
target's binders, its hypotheses and conclusion match exactly. `AnchorAudit.lean` checks that
application directly, without a transport, changed domain, strengthened premise, or placeholder.

The theorem body obtains `Mono` and `Epi` for middle component 2 from the mono and epi four lemmas
on the corresponding truncated diagrams, then applies `CategoryTheory.isIso_of_mono_of_epi`.
Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for both the upstream declaration
and the local feasibility probe. The narrow source scan found no `sorry`, `admit`, user axiom,
`unsafe`, or oracle marker in this body. Full transitive provenance and TCB closure remain later
work; this scoped observation is not such a closure.

`Mathlib.Algebra.FiveLemma` also contains unbundled group and module versions. They are credible
nearby candidates but cannot close this target without improperly specializing the abelian
category. The historical `S1_M_097` wrapper matches, but rev-5.6 makes it discovery-only evidence.

Two anonymous GitHub repository searches returned zero metadata matches. Unauthenticated GitHub
code search returned HTTP 401, so this audit does not turn that access failure into negative
evidence or claim exhaustive external-search saturation. No dependency was fetched, cloned, or
modified.

## Commands and results

Commands ran in this worker clone on 2026-07-12. The Lean command ran from
`Formalizations/Lean`, using the existing canonical `.lake` symlink and pinned artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0002/AnchorAudit.lean` | 0 | exact-type probe elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `rg -n "sorry|admit|axiom|unsafe|oracle" .lake/packages/mathlib/Mathlib/CategoryTheory/Abelian/DiagramLemmas/Four.lean` | 1 | no scoped placeholder or unsafe/oracle token found |
| `git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a1783...a95`, tree `bdc39a...2b` |
| `sha256sum` on the categorical source, legacy source, and mathlib license | 0 | hashes match `anchor-audit.json` |
| two GitHub repository API searches | 0 | zero results, `incomplete_results=false`; response hashes recorded |
| GitHub code-search API query | 22 | HTTP 401 without authentication; recorded as an access limitation |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | repository standard check passed |
| `python3 scripts/stage1_target.py check` | 0 | all 1546 manifest targets passed |
| `python3 scripts/stage1_target.py show THM-M-0002` | 0 | rank 97, lane `hard_mathlib_anchor_and_wrapper`, L0/rework required |
| `git diff --check -- Stage1_Instances/THM-M-0002 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The anchor-audit node is self-tested and supports `M1`: an exact immutable mathlib closure exists
and integration is feasible. It does not claim an accepted proof wrapper, complete trust closure,
H0, R0, audit completion, or theorem completion. The remaining root cut set is the canonical
proof wrapper, full transitive provenance and TCB evidence, and accepted composition receipts.
