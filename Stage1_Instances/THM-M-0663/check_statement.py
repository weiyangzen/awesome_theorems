#!/usr/bin/env python3
import pathlib

path = pathlib.Path(__file__).with_name("Statement.lean")
text = path.read_text(encoding="utf-8")

required = [
    "def OMinimalMonotonicity : Prop",
    "[L.IsOrdered] [L.Structure M] [LinearOrder M] [L.OrderedStructure M]",
    "[DenselyOrdered M] [NoMinOrder M] [NoMaxOrder M]",
    "IsOMinimal (L := L) (M := M) ->",
    "Definable₁ L A ->",
    "Definable L (restrictedGraph A f) ->",
    "Set.PairwiseDisjoint",
    "HasMonotoneBehavior f p",
    "theorem oMinimalMonotonicity_iff",
    "theorem emptyDomainPartition",
]
for needle in required:
    assert needle in text, f"missing canonical statement fragment: {needle}"

mutations = [
    "mutationRemovedOMinimality",
    "mutationChangedDomain",
    "mutationChangedBinderScope",
    "mutationWeakenedConclusion",
]
for mutation in mutations:
    assert f"def {mutation} : Prop" in text, f"missing mutation: {mutation}"

for forbidden in ("sor" + "ry", "axi" + "om", "ad" + "mit"):
    assert forbidden not in text.lower(), f"forbidden token: {forbidden}"

print("statement invariant check: ok")
