# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` supply only:

- name: `赫茨-施坦定理` (Herz-Stein theorem);
- authors/source: Carl Herz / Elias Stein;
- year: 1968;
- claim: `Hardy空间的乘子` (multipliers of Hardy spaces);
- an untrusted `已验证` metadata label.

They provide no title, journal/book, theorem number, page, verbatim statement, definitions,
assumptions, proof, errata, or formal artifact. The manifest expressly records the status label as
untrusted. It therefore supplies no H0 or machine-proof credit.

## Discovery boundary

A bibliographic discovery query found Carl Herz's later *Generalisations de la notion des classes
Hp de Hardy* (1974, DOI `10.1007/BFb0060614`). This is only a candidate locator showing relevant
Herz/Hardy-space literature; its date does not match the repository's 1968 row, it was not
inspected as the intended theorem, and it is not adopted as a primary source. The exact 1968
Herz/Stein attribution remains unresolved.

The statement phase must locate an immutable primary source matching the attribution, transcribe a
numbered theorem with edition/page, and audit assumptions, definitions, corrections, and errata.
Until then even the provisional quantifier order would be invented, so no canonical statement is
asserted.

## Crosswalk

| Repository phrase | Mathematical choice still required | Lean component | Status |
|---|---|---|---|
| Hardy space | ambient setting, `H^p` construction, representatives/equality | new or identified Hardy-space API | unresolved |
| multiplier | transform convention and operator induced by a symbol | mathlib has a Schwartz/distribution multiplier construction | ingredient only |
| theorem | hypotheses, exponent/dimension range, boundedness conclusion and norm constant | exact `Prop` with ordered binders | unresolved |
| Carl Herz / Elias Stein | joint result, separately originated results, or later eponym | no machine component | unresolved attribution |
| 1968 | publication or provenance date | no machine component | unsupported by an inspected source |
| `已验证` | ambiguous source metadata | no accepted declaration or proof body | explicitly untrusted |

## Pinned Lean boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides
`Mathlib.Analysis.Distribution.FourierMultiplier` and generic Lp infrastructure. The local probe
elaborates these declarations, but none is crosswalked to the unresolved human claim. This is an
intake search, not the later immutable anchor audit.

