# THM-M-0397 Statement Freeze

## Canonical target

The repository wording, "effective solution methods for Diophantine equations",
does not name one Diophantine equation. `Statement.lean` therefore freezes the
common method theorem rather than silently choosing an application: a concrete
nonzero linear form in chosen logarithms of nonzero algebraic complex numbers,
a strict Baker lower bound for that form, and a problem-specific reduction of
all solutions to a computably enumerated height ball produce a finite executable
list containing exactly the solutions.

`Application` keeps the two mathematical inputs explicit. `HasBakerLowerBound`
is the analytic lower-bound premise; `reduce_solution` is the equation-specific
reduction. Neither is manufactured by the target. The conclusion identifies
membership in `solutionList`, formed by filtering `heightBall searchBound`, with
the full solution predicate.

`statement_iff_expanded` checks the complete proposition expansion.
`mem_solutionList_iff` checks that list membership retains both boundedness and
the solution predicate. These checks do not prove `Statement`.

## Mutation boundary

Dropping algebraicity, nonzeroness, or the exponential equations changes the
logarithmic-form substrate. Dropping the Baker premise makes the application
unconditional. Dropping `reduce_solution` disconnects the analytic bound from
the Diophantine problem. Dropping `heightBall_spec`, decidability, or filtering
weakens an effective exact enumeration to abstract finiteness. Selecting a
particular equation would substitute a narrower theorem not present in the
source wording.

This phase establishes elaboration of the exact method-level proposition only.
It does not establish a lower-bound theorem, an application reduction, H0,
machine proof closure, audit completion, or theorem completion.
