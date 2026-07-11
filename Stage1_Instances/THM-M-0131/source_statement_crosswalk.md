# Source-statement crosswalk

| Claim component | Repository anchor | Candidate interpretation | Intake assessment |
|---|---|---|---|
| Name | Stage0 and Stage1: `志村对应` | Classical Shimura correspondence | Name alone is not an exact claim |
| Content gloss | Stage0 line for THM-M-0131 and Stage1 legacy slot: `椭圆曲线与模形式的对应` | Modularity theorem for elliptic curves | Broad prose, with no field, hypotheses, or precise conclusion |
| Claimed historical origin | Stage0: Goro Shimura / Yutaka Taniyama, 1955 | Taniyama-Shimura(-Weil) conjecture/theorem | This points toward modularity and overlaps the separately listed THM-M-0132 |
| Formal status label | manifest: untrusted `已验证` | Human proof may exist | Explicitly untrusted; supplies neither H0 nor machine evidence |
| Lean candidate | none in the repository record | Scheme/modular-form APIs or a future wrapper | No exact declaration may be selected before scope is resolved |

There are two materially different readings. The classical Shimura correspondence normally relates
modular forms of half-integral weight to modular forms of integral weight. The repository's content
gloss instead describes the modularity correspondence for elliptic curves, while its attribution
and date also resemble the Taniyama-Shimura conjecture represented separately by `THM-M-0132`.
They are not interchangeable theorem statements.

Consequently this intake does not nominate a primary mathematical source: doing so before choosing
the theorem family could manufacture a source-to-statement match. The next phase requires an
authoritative source decision and then an edition/theorem/page/assumptions/errata crosswalk. Until
that occurs the honest classifications are `H4` (source/claim unresolved) and `M4` (no exact Lean
target). No proof closure, anchor status, or transport equivalence is claimed.
