# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| “Nakajima geometry” | Repository `Docs/researches/math_theorems.md`, entry “中岛几何” | none | A title-like label; not an exact claim |
| “moduli spaces of quiver representations” | Same entry and `Docs/Stage0_Blueprint.md` | none | Object description only; required parameters and conclusion are absent |
| 1994 attribution | H. Nakajima, *Instantons on ALE spaces, quiver varieties, and Kac-Moody algebras*, Duke Math. J. **76** (1994), 365–416, DOI `10.1215/S0012-7094-94-07613-8` | none | Plausible primary source discovered; no numbered theorem has yet been selected or checked |
| Exact root proposition | not present in repository metadata | none | Hard blocker: selecting among distinct results would invent or substitute the target |

The source candidate contains multiple constructions and theorems, so its paper title and page
range do not establish `H0`. The statement phase must inspect the primary text, select a numbered
statement with its complete assumptions, explain its distinction from `THM-M-0143`, check errata,
and obtain independent review. Only then may it define a canonical Lean target and mutation tests.

The repository label `已验证` is explicitly untrusted by the rev-5.6 manifest. No public formal
artifact, Lean declaration, source-proof closure, or equivalence transport is claimed here.
