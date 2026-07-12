# Exact-statement gate: blocked

Item: `S56-M-0789-STATEMENT`  
Theorem: `THM-M-0789`  
Base revision: `32404187d6cee70b44ae90adf8d0d765752e5149`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
only mathematical wording is `可测基数与超滤子` ("measurable cardinals and ultrafilters"). The
accepted intake correctly freezes this as a topic rather than selecting a proposition. The record
provides no primary-source edition, theorem/page, definition, ordered binders, hypotheses, or
conclusion.

Several inequivalent roots remain compatible with that wording: a definition or characterization
by a nonprincipal kappa-complete ultrafilter; an equivalence with a nontrivial kappa-additive
zero-one measure; Ulam's result that a measurable cardinal is inaccessible; or an assertion that a
measurable cardinal exists. The last is a large-cardinal assumption rather than a theorem of the
ordinary base theory. Choosing any one would invent or substitute mathematics.

Even the ultrafilter reading leaves material choices open: whether the carrier is a cardinal or an
equipotent type, completeness under families indexed by sets of cardinality less than kappa,
nonprincipality versus uniformity, uncountability and other boundary conditions, universe levels,
and whether the conclusion is a definition, equivalence, existence claim, or consequence.
Consequently there is no canonical expression to serialize or hash and no sound
removed-hypothesis, changed-domain, changed-binder-scope, or boundary mutation suite. The rev-5.6
Lean statement gate fails before proof evidence may be inspected; machine debt remains `M4`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. It confirms that
mathlib exposes `Cardinal`, `Ultrafilter`, `CardinalInterFilter`, and
`Cardinal.IsInaccessible`. Its final function is explicitly only a candidate shape: it omits a
source-selected nonprincipality/uniformity condition and asserts no theorem. A bounded search of
the pinned mathlib source found no declaration named `MeasurableCardinal` or for "measurable
cardinal". These checks distinguish an available encoding substrate from a missing mathematical
statement; they receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The canonical `.lake` artifacts were used read-only;
no update, build, fetch, clone, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0789` | 0 | rank 794; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID and Chinese/English labels | 0 | found only the underspecified metadata and intake records; no exact proposition |
| pinned-mathlib `rg` search for `measurable cardinal` and `MeasurableCardinal` | 1 | expected no-match exit; no named API found |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0789/IntakeProbe.lean` | 0 | candidate cardinal/filter APIs elaborated; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0789 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom |

## Retry condition

An accountable reviewer must preserve and hash an immutable primary source, select and transcribe
one exact result with all incorporated definitions and assumptions, audit errata, and independently
approve the source mapping. A later statement run can then encode that same claim, minimize pinned
imports, fingerprint the elaborated expression, check alternate transports, and run all four
required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The root
remains `[H3, M4, R4]`; `audit_complete` and `theorem_complete` remain false. The assigned
deliverable is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
