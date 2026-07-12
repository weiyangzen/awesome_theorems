# Anchor-audit validation record

Item: `S56-M-0650-ANCHOR_AUDIT`  
Base revision: `737d00e2fcd766790dfe7d675dfb8e279f059733`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact proof-bearing
candidate `FirstOrder.Language.Substructure.isElementary_of_exists` in
`Mathlib/ModelTheory/ElementarySubstructures.lean:126-132`. Its premise and conclusion match the
canonical target binder-for-binder after unfolding the two local proposition definitions. The direct body
delegates through the natural subtype embedding to
`FirstOrder.Language.Embedding.isElementary_of_exists`, whose retained source body performs structural
induction over bounded formulas. The substructure wrapper was introduced at immutable mathlib commit
`a5732e8fe6e2c7b67bd4e9f49e505e991ca68df4`; the terminal embedding theorem originates at
`26d572805b336851ae1451bae19bc6eacac5e3d4`. The repository pin, not either historical commit alone,
is the audited executable revision.

`AnchorAudit.lean` locally checks the exact target shape through the pinned theorem. For that check,
the substructure theorem, and the terminal embedding theorem, Lean reports precisely the standard
foundation profile `propext`, `Classical.choice`, and `Quot.sound`, with no target-specific axiom. The bundled
`toElementarySubstructure` definition is recorded but excluded as an alternate result encoding. A search
of every installed pinned dependency found no other candidate family. Public Sourcegraph, GitHub, and
grep.app lanes supplied no usable response because of empty responses or rate limits; they are recorded as
blocked lanes rather than global negative evidence.

The root is therefore classified `M0-P_candidate`: the exact pinned proof is feasible for the later proof
phase. This anchor audit does not freeze the obligation registry, accept proof credit, establish H0, or
claim theorem completion. The downstream proof phase must create the canonical wrapper and the validation
and release phases must audit its full provenance/trust closure.

## Commands and exact outcomes

All commands used the existing pinned `.lake` artifacts. No update, build, clone, or fetch was performed.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard passed: 15 assurance groups and 1,546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0650` | 0 | rank 696; planned; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0650/Statement.lean` | 0 | exact statement, checked transport, mutations, and explicit expression re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0650/AnchorAudit.lean` | 0 | exact pinned wrapper and three candidate probes elaborated; all three axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0650/check_anchor_audit.py` | 0 | exact anchor, terminal body, source hashes, Apache-2.0 license file, manifest pin, and installed mathlib HEAD agreed |
| `find Formalizations/Lean/.lake/packages ... \| xargs rg -l -i 'Tarski.?Vaught\|isElementary_of_exists'` | 0 | only pinned mathlib `ElementaryMaps`, `ElementarySubstructures`, and `Skolem` matched |
| Sourcegraph public search requests for `Tarski-Vaught` and `isElementary_of_exists` in Lean | 0 | no usable payload; blocked lane, not a negative claim |
| GitHub/grep.app public search requests | 22 | HTTP 403/429 rate limits; blocked lanes, not negative claims |
| `python3 -m json.tool Stage1_Instances/THM-M-0650/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0650 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open downstream gate

The anchor audit is self-tested and ready for master review. The theorem remains unproved in the rev-5.6
workflow until the obligation tree is frozen and a proof-phase wrapper receives exact-type, provenance,
trust, composition, and later release evidence. Any change to the target hash, toolchain, mathlib pin, or
candidate body invalidates this audit.
