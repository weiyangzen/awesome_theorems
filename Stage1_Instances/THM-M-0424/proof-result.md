# THM-M-0424 proof-phase result

Item: `S56-M-0424-PROOF`. Base revision:
`427e0fa01ba0ea293b1ca663a4308d3acf9d04a4`.

## Verdict

The proof phase is **blocked** and is not self-tested as complete. No proof body
was added, and no worker self-test manifest is emitted.

The frozen exact target requires an inhabitant of `BrauerGroupLawData` for
every field. Its root cut set contains the ten substantive construction and
law packages `M0424-C-TENSOR-ALG`, `M0424-C-TENSOR-CSA`,
`M0424-C-TENSOR-CONGR`, `M0424-C-ONE`, `M0424-C-OPPOSITE`,
`M0424-L-DESCENT`, `M0424-L-ASSOC`, `M0424-L-COMM`, `M0424-L-UNIT`, and
`M0424-L-INVERSE`. None has a terminal proof body in the frozen registry.

The pinned mathlib file `Mathlib.Algebra.BrauerGroup.Defs` supplies only
`CSA`, `IsBrauerEquivalent`, its setoid, and the quotient `BrauerGroup`. Its
module documentation explicitly leaves the tensor-product abelian group law
as TODO 1. A source-wide search of the existing pinned dependency closure found
no other implementation of `BrauerGroup`, `IsBrauerEquivalent`, or the group
law. The neighboring tensor API proves only converses extracting centrality
from an already-central tensor product; it does not prove that the tensor
product of two central simple algebras is central and simple. Therefore the
first failed proof gate is `M0424-C-TENSOR-CSA`. The downstream congruence,
descent, group laws, and inverse theorem cannot be truthfully implemented from
the available pinned bodies.

There is also a target-level universe blocker at `M0424-C-ONE`: the frozen
interface demands `oneRep : CSA.{u,v} K` together with an algebra equivalence
from its `Type v` carrier to arbitrary `K : Type u`, with no relation between
`u` and `v`. The usual `ULift` construction has carrier universe `max u v` and
does not supply a `Type v` representative when `u` is larger than `v`. A proof
retry must first correct and re-freeze this universe boundary (normally by
relating the universes or using a carrier in `Type (max u v)`). Doing that in
this phase would replace the already frozen target.

Supplying `BrauerGroupLawData` as an assumption, axiom, bodyless declaration,
or opaque package would violate the no-placeholder rule. A retry requires a
pinned Lean 4 implementation of the Brauer group law or local proofs of the
tensor-CSA construction and every downstream frozen obligation. No moving
dependency was fetched.

## Scoped validation

Validation ran in the worker clone on 2026-07-12 and reused only the existing
pinned Lake artifacts. No update, build, clone, fetch, or `.lake` mutation was
performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy
    slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0424
  exit 0
  execution rank 78; lifecycle planned; baseline L0/rework_required;
    theorem_complete false

python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py
  exit 0
  PASS THM-M-0424 obligation tree: 18 obligations, 35 typed edges
  registry denominator sha256:
    83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00
  root closure: open (M3); nine substantive construction/law packages remain
    in the root cut set

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0424/ObligationTree.lean
  exit 0
  all frozen LawData projections elaborated; the conditional composition
    certificate reported [propext, Classical.choice, Quot.sound]

rg -n -i 'BrauerGroup|Brauer group|IsBrauerEquivalent|Brauer equivalen|CSA_Setoid' \
  Formalizations/Lean/.lake/packages --glob '*.lean'
  exit 0; 28 matching lines, all definition/documentation imports or the
    audited BrauerGroup.Defs implementation; no terminal group-law body

rg -n 'TensorProduct.*IsSimpleRing|IsSimpleRing.*TensorProduct|TensorProduct.*IsCentral|IsCentral.*TensorProduct' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
  exit 0; one converse-centrality implementation line only, no tensor-CSA body
```

These commands validate the frozen target and its conditional composition,
not the missing substantive premise. Root debt remains `M3`, theorem
completion remains false, and master acceptance is not claimed.
