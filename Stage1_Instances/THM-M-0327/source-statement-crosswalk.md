# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` records the Chinese title `邓福德-佩蒂斯定理`, attributes it to
Nelson Dunford and Billy Pettis, dates it to 1940, and gives only `弱紧算子的特征`
("characterization of weakly compact operators"). Stage0 repeats that gloss while marking exact
definitions, hypotheses, proof path, equivalent formulations, axioms, and existing formal artifact
as `待补充`. The rev-5.6 manifest retains `已验证` only as untrusted source metadata.

This does not identify an edition, theorem number, page, ordered binders, hypotheses, conclusion,
proof, or errata. In particular, the named theorem is also commonly associated with the
uniform-integrability characterization of relatively weakly compact subsets of `L^1`; related
operator and Banach-space-property formulations are not interchangeable. Intake does not choose
one by reputation.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "weakly compact" | compactness for the weak topology or relative weak compactness | `WeakSpace`, `IsCompact`, closure/image operations | family identified; exact topology and set open |
| "operators" | bounded linear map between source-specified Banach spaces | `ContinuousLinearMap`; weak topology on its image/codomain | domains and criterion absent |
| Dunford-Pettis theorem | weak compactness criterion for an `L^1` family | `MeasureTheory.Lp`, `MeasureTheory.UniformIntegrable` or a source-matched variant | competing standard reading |
| "characterization" | one implication or an iff with all side conditions | an exact `Prop` with ordered binders and hypotheses | absent from repository record |
| 1940 / named authors | bibliographic discovery lead | no machine-proof credit | exact publication and locator open |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected as evidence |

## Source and Lean boundary

The source phase must identify and independently inspect a primary publication or an authoritative
edition that states the intended proposition, recording its locator, conventions, assumptions,
proof boundary, and errata. Secondary textbook variants may guide discovery but cannot silently
replace the repository target.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake probe
imports weak-topology, compact-operator, and uniform-integrability modules and checks representative
types. `IsCompactOperator` uses the topology supplied on its codomain, so its norm-topology use is
not by itself the required weak-compactness claim. The probe establishes API availability only; the
later anchor audit must inventory exact declarations and terminal proof provenance.
