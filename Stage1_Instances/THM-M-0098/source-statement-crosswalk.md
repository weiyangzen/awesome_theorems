# Source-statement crosswalk

## Authoritative repository record

`Docs/researches/math_theorems.md:719-724`, introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, contains the entire source record:

- title: `朗兰兹纲领基本引理`;
- proposer: Robert Langlands;
- date: 1979;
- statement: `自守表示与伽罗瓦表示的对应`;
- importance: high;
- source status: `已验证`.

`Docs/Stage0_Blueprint.md:2794-2819` is a projection of the same metadata and explicitly leaves
definitions, assumptions, proof route, foundations, and machine artifact unresolved. The rev-5.6
manifest carries `已验证` only in `source_status_untrusted`. These repository records are secondary
inventory evidence, not a primary theorem source or an `H0` crosswalk.

## Conflict crosswalk

| Repository component | Mathematical reading | Lean surface required | Intake result |
|---|---|---|---|
| title: "fundamental lemma" | Langlands-Shelstad endoscopy and an equality of normalized orbital integrals | local fields, reductive/endoscopic data, matching regular semisimple classes, measures, transfer factors, test functions | materially absent from the literal statement; no root selected |
| statement: "automorphic and Galois representations correspond" | local/global Langlands reciprocity or one of its proved/conjectural directions | automorphic representations, Galois/Weil parameters, coefficient/topology/ramification data, compatibility laws | materially different from the title and not a single binder-complete theorem |
| Robert Langlands / 1979 | historical locator | immutable publication, exact theorem or conjecture passage, edition and passage digest | no bibliographic identity supplied; year does not resolve the collision |
| `已验证` | catalog classification | accepted source review or kernel receipt | explicitly untrusted; no credit |

## Discovery candidates, not accepted sources

- For the literal gloss, R. P. Langlands, *Problems in the Theory of Automorphic Forms*, Lecture
  Notes in Mathematics 170, Springer (1970), pp. 18-61, is a repository-local discovery candidate
  already recorded for separate target `THM-M-0430`. No exact passage, immutable edition digest,
  premise mapping, or errata review is accepted here.
- For the title, B. C. Ngo, *Le lemme fondamental pour les algebres de Lie*, Publications
  Mathematiques de l'IHES 111 (2010), 1-169, DOI `10.1007/s10240-010-0026-7`, is a primary proof
  source candidate already recorded for separate target `THM-M-0434`. It neither explains the
  catalog's automorphic/Galois gloss nor transfers that target's scope to `THM-M-0098`.

These candidates demonstrate that both readings are mathematically meaningful. They do not show
which reading this source record intended, and citations alone cannot establish `H0`.

## Existing Lean boundary

The bounded intake probe checks pinned mathlib objects adjacent to both readings. The repository
also contains `S1_M_058.lean` for the reciprocity sibling and `S1_M_083.lean` for the Fundamental
Lemma sibling. Both legacy modules explicitly describe statement-shape or interface boundaries, not
source-faithful terminal proofs. They are not imported, credited, or treated as alternate encodings
for this target.

Before source acceptance, an independent reviewer must pin the intended primary source, record its
edition and digest, pinpoint the theorem/conjecture and every referenced definition, audit errata,
and map every domain, ordered binder, hypothesis, normalization, boundary case, and conclusion to
the chosen Lean expression. Until then the source-statement crosswalk is intentionally open.
