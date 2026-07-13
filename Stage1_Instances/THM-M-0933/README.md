# THM-M-0933 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Olson定理`
(`Olson theorem`). The catalog gives John Olson, 1969, and only the gloss `有限阿贝尔群的Davenport常数`
(`the Davenport constant of finite abelian groups`). It does not state a formula, define the
constant, select a class of finite abelian groups, or identify a source theorem.

The strongest source lead inspected at intake is David J. Grynkiewicz, arXiv:2208.12895v1 (2022),
Theorem 1.5. It explicitly calls the following a classical result of Olson and cites Olson's 1969
paper, *A Combinatorial Problem on Finite Abelian Groups I*, pages 8-10:

```text
If G is a finite abelian p-group, then D(G) = D*(G).
```

The same paper defines `D(G)` as the least length forcing a nonempty zero-sum subsequence and,
after choosing an invariant-factor decomposition, defines `D*(G) = 1 + sum_i (n_i - 1)`. Its
pages 17-18 give a complete modern proof. Crossref and publisher metadata confirm the cited Olson
paper, and CORE exposes its abstract saying the sequence problem is answered for p-groups. The
original three-page proof body was not retrievable in this run, and the repository gloss does not
say whether it intends this p-group equality, the rank-two equality also associated with Olson,
the special value `D((Z/nZ)^2) = 2n - 1`, or a broader Davenport-constant topic. Intake therefore
does not silently select one candidate as the canonical root.

The provisional vector is `[H1, M4, R4]`. `H1` records a pinpointed modern proof and original
primary-source lead whose exact identity with the catalog root, original proof, corrections, and
independent review remain open. `M4` records that no exact Olson/Davenport declaration was found by
the bounded pinned-tree search; the Lean probe authenticates only adjacent finite-group,
multiset-sum, submultiset, and zero-sum APIs. `R4` records that no readable proof can attach to an
unselected root.

`scope-map.md` freezes the proposition-changing choices, `source-statement-crosswalk.md` records
the source and Lean boundaries, and `task-dag.json` leaves all downstream phases open. No accepted
execution state, exact canonical Lean statement, proof credit, audit completion, theorem
completion, or master acceptance is claimed.
