# THM-M-0956 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0956`, the catalog label
`Erdős-Turán构造` (Erdos-Turan construction). The repository attributes it to Paul Erdos and Pal
Turan in 1941 and supplies only the gloss `Sidon集的构造` ("construction of a Sidon set"). It does
not cite a source or specify the construction, Sidon convention, ambient domain, parameters,
quantifiers, size bound, or boundary cases. Its `已验证` field is untrusted metadata under rev-5.6.

## Intake result

The matching primary paper was inspected for source discrimination: P. Erdos and P. Turan, "On a
Problem of Sidon in Additive Number Theory, and on some Related Problems," *Journal of the London
Mathematical Society* s1-16(4) (1941), 212-215, DOI `10.1112/jlms/s1-16.4.212`. Section I on page
213 gives a finite prime-indexed construction: for prime `p` and `1 <= k <= p - 1`, take
`a_k = 2*p*k + r_k`, where `r_k` is the least positive residue of `k^2` modulo `p`; the resulting
`p - 1` positive integers are below `2*p^2`, and distinct unordered index pairs have distinct sums.

That exact construction is a strong candidate for the catalog target, but it is not yet the
canonical statement. The catalog does not say whether it selects this finite construction, its
asymptotic consequence for the extremal counting function, or a later set/group formulation. The
scan has no independent source review, and its displayed asymptotic formulas require visual
transcription before any broader consequence can be frozen.

## Formal boundary

The provisional vector is `[H1, M4, R4]`. `H1` records an inspected matching primary source whose
exact target selection, definition crosswalk, transcription, errata status, and independent review
remain open. `M4` records that no source-identical Lean target or proof artifact is credited; `R4`
records that no reviewed readable proof reconstruction exists. The canonical mathematical
statement and Lean target therefore remain null.

`instance.json` is the structured scope authority. `scope-map.md` freezes proposition-changing
choices and exclusions, `source-statement-crosswalk.md` records the source clauses and boundaries,
and `task-dag.json` keeps all six downstream phases open. `IntakeProbe.lean` authenticates only
adjacent pinned finite-set, interval, pairwise, big-operator, and square-root APIs. No H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
