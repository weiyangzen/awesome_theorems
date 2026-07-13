# THM-M-0925 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`斐波那契数列` (Fibonacci sequence). The catalog supplies only the gloss `递推序列的经典例子`
("a classic example of a recursive sequence"), attributes it to Leonardo Fibonacci in 1202, and
labels it `已验证`. An object name and an example description are not a truth-valued proposition
with ordered binders, hypotheses, and a conclusion. The verified label is explicitly untrusted
under rev-5.6.

The received wording does not choose a recursive definition, a theorem that the named sequence
satisfies a recurrence, an existence-and-uniqueness characterization, Fibonacci's rabbit-counting
problem, or any of the many identities and limit results about the sequence. It also leaves the
zero-based versus one-based indexing convention and value domain open. Intake does not silently
replace those missing choices with a familiar formula.

Boncompagni's 1857 transcription of *Liber Abbaci* was inspected through an authenticated BSB
scan. Printed pages 283-284 state the rabbit model, calculate monthly totals through 377, and
explicitly describe repeated addition. Its historical indexing starts with one initial pair and
then 2 pairs in the first month, so a modern `Nat.fib` encoding needs a shift. MacTutor-hosted
historical studies confirm that Fibonacci displayed the sequence rather than the modern formula.
These sources are strong scope leads, not an original 1202 manuscript, a complete proof crosswalk,
or an independently accepted target. OEIS A000045 supplies an additional modern lead but currently
has inconsistent locators for a remark in Laurence Sigler's closed-access translation.

Pinned mathlib defines `Nat.fib` and proves `Nat.fib_zero`, `Nat.fib_one`, and
`Nat.fib_add_two`. `IntakeProbe.lean` authenticates those interfaces at the pinned revision. They
are strong definition/statement candidates, but no source-approved canonical root has been
selected, so they receive no wrapper or proof credit for this target.

The provisional catalog-target vector is `[H5, M3, R4]`. `H5` classifies only the literal catalog
wording as not yet a stable proposition; it does not refute the Fibonacci recurrence or question
the well-established mathematics. `M3` records pinned definition and recurrence interfaces, not an
exact target or accepted proof. All six downstream phases remain open. No H0, M0, R0, accepted
state, audit completion, theorem completion, or master acceptance is claimed.
