# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| "Nakajima quiver varieties" | Repository `Docs/researches/math_theorems.md`, entry "中岛箭图簇" | none | Object-family label, not an exact claim |
| "construction of moduli spaces of quiver representations" | Same entry and `Docs/Stage0_Blueprint.md` | none | Construction gloss omits input data, conventions, and a conclusion |
| 1994 attribution | H. Nakajima, *Instantons on ALE spaces, quiver varieties, and Kac-Moody algebras*, Duke Math. J. **76** (1994), 365-416, DOI `10.1215/S0012-7094-94-07613-8` | none | Plausible primary source discovered; no exact definition/result/page has been checked |
| Exact root proposition | absent from repository metadata | none | Hard blocker: choosing a construction property or consequence now would invent or substitute the theorem |

The candidate paper contains definitions, geometric constructions, and multiple results. Its title,
page range, and attribution cannot establish `H0`. The statement phase must inspect a fixed primary
text, select and pinpoint an exact proposition, transcribe all assumptions, map every source notion
to the chosen Lean encoding, search corrections/errata, and receive independent review. It must
also explain the non-duplication boundary with `THM-M-0142`.

The manifest's `source_status_untrusted` value is not evidence. No public formal artifact, Lean
declaration, source-proof closure, equivalence transport, or theorem completion is claimed here.
