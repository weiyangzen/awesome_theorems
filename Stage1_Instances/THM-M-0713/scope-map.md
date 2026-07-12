# Scope map

## Repository claim

`Docs/researches/math_theorems.md` names Yuri Matiyasevich, gives 1970, and states only
`希尔伯特第10问题的否定解` ("the negative solution of Hilbert's tenth problem"). Stage0
repeats this phrase while leaving definitions, assumptions, proof route, equivalent formulations,
axioms, and formal artifacts open. The manifest's `已验证` is explicitly untrusted metadata.

## Candidate claim boundaries

- **Matiyasevich step:** exponentiation on natural numbers has a Diophantine graph. Pinned mathlib
  calls `pow_dioph` a version of Matiyasevich's theorem.
- **MRDP characterization:** every recursively enumerable set is Diophantine. The adjacent target
  `THM-M-0714` separately names this theorem, so intake may not silently duplicate it here.
- **Hilbert-tenth consequence:** no algorithm decides whether an arbitrary integer polynomial has
  an integer zero. This is the literal effect of the repository gloss, but it requires a fixed
  computation model, input encoding, solvability predicate, and reductions from MRDP.

These are dependencies or consequences, not interchangeable statement spellings. Intake does not
select one without a primary-source pinpoint and an explicit decision about the neighboring target.

## Decisions required at statement freeze

The statement phase must freeze the exact source proposition; natural versus integer variables;
finite arity and polynomial representation; exponentiation convention including zero cases; the
definition of Diophantine set/function; the recursively enumerable or computably enumerable model;
the encoded algorithm and decision contract; all transports between encodings; binder order;
minimal imports; foundation/choice policy; and the exact conclusion.

## Explicit exclusions

- Treating `pow_dioph` alone as the negative solution of Hilbert's tenth problem.
- Importing the full MRDP theorem under this ID without reconciling `THM-M-0714`.
- Replacing arbitrary multivariate integer-polynomial solvability by a convenient fixed equation or
  natural-number variant without checked two-way transports.
- Defining "undecidable" as the desired conclusion or assuming the nonexistence of an algorithm.
- Crediting a title, `已验证` label, TODO comment, citation, or successful API probe as root proof.

No canonical Lean target is frozen at intake.
