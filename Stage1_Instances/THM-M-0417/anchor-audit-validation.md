# Anchor-audit validation record

Item: `S56-M-0417-ANCHOR_AUDIT`  
Base revision: `1ec654c416270f261b365f46f5f2409b65d3f839`

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact terminal
theorem `MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure` in
`Mathlib.MeasureTheory.Group.GeometryOfNumbers`. The checked theorem
`mathlibCandidateClosesFrozenTarget` transports it directly to the statement-phase definition with
no changed binder, hypothesis, inequality, or conclusion. The upstream body reduces the scaled
half-body to Blichfeldt's theorem and then uses symmetry and convexity to produce the nonzero
lattice point. Its source body is present, contains no `sorry`, `admit`, or axiom declaration, and
both upstream and wrapper axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`.

The legacy `S1_M_072` theorem and Atlas's immutable `minkowski_lattice_point` are duplicate one-step
wrappers around that same mathlib declaration; they earn no distinct terminal-body credit. Atlas
uses the identical Lean and mathlib revisions but is not integrated because it adds nothing and its
license is CC BY-NC 4.0 with a no-training rider. The compact `<=` mathlib theorem is adjacent rather
than interchangeable because it adds compactness, discrete-topology, and nontriviality hypotheses.

Thus the audit locates an `M0-W` candidate already inside the pinned local dependency closure. This
phase does not accept M0-W: proof-node integration, complete dependency/body provenance, obligation
composition, trust validation, human-source and readability closure, and master acceptance remain
later gates. No theorem-completion claim is made.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Lean used only the existing pinned `.lake`
artifacts; no update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0417/AnchorAudit.lean` | 0 | Exact wrapper and three candidates elaborated; upstream and wrapper axiom sets were `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0417/check_anchor_audit.py` | 0 | Exact wrapper markers, terminal body, prohibited-token scan, source blob/hash, manifest pin, and installed mathlib HEAD agreed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0417/Statement.lean` | 0 | Frozen target, exact-type fixture, and four mutations re-elaborated |
| pinned-source `rg` search for Minkowski and exact declaration names | 0 | Exact strict and compact mathlib terminals, downstream number-field uses, and unrelated Minkowski inequalities/functionals classified |
| Sourcegraph exact-name query | 0 | 12 matches across mathlib4/mathlib3/Atlas paths; response SHA-256 `af004073...bab21` |
| GitHub repository query for `"Minkowski theorem" lean` | 0 | One distinct Hasse-Minkowski project; complete response SHA-256 `91c8b241...75a18` |
| GitHub code query for `"Minkowski Convex Body" language:Lean` | 0 | HTTP 401 authentication blocker; response SHA-256 `b7dbd173...65e29e` |
| GitHub API inspection of `facebookresearch/atlas-lean@34ffed396...` | 0 | Exact wrapper, Lean v4.29.0, identical mathlib pin, immutable commit, and restrictive license recorded |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0417` | 0 | rank 72, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0417` | 0 | no whitespace errors |

## Remaining boundary

The next phase may use C01 as the unique terminal anchor when freezing its proof, provenance, and
workflow obligations. It must not double-count the legacy or Atlas aliases. The later proof and
validation nodes must independently establish the full transitive dependency closure, trust and
TCB policy, and reproducible receipt before the root can be accepted as `M0-W`.
