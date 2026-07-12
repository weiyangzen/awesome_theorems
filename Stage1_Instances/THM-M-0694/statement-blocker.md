# Exact-statement gate: blocked

Item: `S56-M-0694-STATEMENT`  
Theorem: `THM-M-0694`  
Base revision: `2ff2721a0184cf5f856054cb7d46b10dbc703f5a`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire theorem-specific claim is the label `自然演绎` ("natural deduction") and the gloss
`自然风格的证明系统` ("a natural-style proof system"). A second inventory calls it a natural
deduction system and disagrees on the date (1935 rather than 1934). The classification notes add
only that introduction and elimination rules are paired and proofs are tree-shaped. These records
identify a proof-system family, not a proposition with ordered binders, hypotheses, and a
conclusion.

The accepted intake correctly records proposition-critical choices that remain open:

- propositional versus first-order syntax, and minimal, intuitionistic, or classical logic;
- formula, context, substitution, and derivation representations;
- introduction, elimination, structural, absurdity, and classical rules, including side
  conditions;
- empty contexts and signatures, exchange/weakening/contraction policy, and derivation equality;
- whether the claim is a particular derivability result, soundness, completeness, normalization,
  consistency, admissibility, the subformula property, or equivalence with another calculus.

These alternatives have materially different domains and conclusions. Selecting a familiar
calculus and metatheorem would substitute invented mathematics for the source target. Treating
Lean's ambient proposition constructors as the intended object calculus, or defining an inductive
calculus and merely proving one of its constructors, would also be a proxy rather than the exact
claim. The intake's `IntakeProbe.lean` is explicitly discovery-only and supplies no statement
identity or proof credit.

Consequently there is no canonical proposition against which minimal imports, an elaborated
expression hash, alternate-encoding transports, or the required removed-hypothesis,
changed-domain, binder-scope, and boundary mutations can be evaluated. No new Lean declaration,
`sorry`, axiom, placeholder predicate, weakened special case, or broadened target was introduced.
Machine state remains `M4`; this phase claims no accepted receipt, audit completion, dependent-node
credit, or theorem completion.

## Required unblock

An accountable source reviewer must preserve and independently review an immutable primary-source
edition or exact accepted transcription, identify a specific definition and numbered or displayed
result, reconcile the 1934/1935 attribution, and record errata. The crosswalk must freeze the object
language, calculus, contexts, every inference rule and side condition, semantics if applicable,
ordered binders, hypotheses, conclusion, and degenerate cases. Only then can a statement worker
encode the source-bound proposition, minimize pinned imports, fingerprint its elaboration, check
transports, and run meaningful statement mutations.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical pinned
`.lake` artifacts were used read-only; no update, build, clone, fetch, or dependency mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0694` | 0 | rank 735, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -C 4 '自然演绎\|自然推理系统\|natural deduction\|Natural deduction' Docs/researches Docs/Stage0_Blueprint.md Formalizations/Lean/AwesomeTheorems --glob '!**/.lake/**'` | 0 | found only topic-level inventory/classification records and unrelated uses as a proof method; no exact theorem statement |
| `rg -n '(^|[[:space:]])(sorry|admit)([[:space:]]|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0694` | 1 | no proof escape or axiom declaration (`rg` exit 1 means no match) |

First failed gate: exact source-statement identity, before Lean target elaboration. There is no
applicable `lake env lean <statement>.lean` check because creating such a statement would require
making the prohibited choices above. The assigned phase is not genuinely self-tested to its
completion gate, so no `.stage1-worker-selftest.json` is emitted.
