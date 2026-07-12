# THM-M-1382 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`最小作用量原理` (principle of least action). The catalog attributes the entry to William
Hamilton in 1834 but supplies only the gloss `物理系统的变分原理` (a variational principle for
physical systems). That wording names a family of principles; it is not a binder-complete,
truth-valued proposition.

The ambiguity is material. "Least" may mean a local or global minimum, a stationary first
variation, or Hamilton's fixed-endpoint principle. "Action" may mean the modern time integral of a
Lagrangian or Hamilton's fixed-energy accumulated living force. A target could assert a variational
characterization of trajectories, a necessary Euler-Lagrange condition, its converse, existence of
a minimizer, or an equivalence under additional regularity. These claims have different domains,
hypotheses, boundary conditions, and degenerate cases.

Hamilton's 1834 *On a General Method in Dynamics* was inspected as an authoritative source-family
discriminator. Its Section 3 explicitly says that "least action" would be better called
"stationary action," but its action, energy constraint, endpoint convention, and law of varying
action do not by themselves select the modern `integral L(t,q,q') dt` theorem commonly associated
with Hamilton's principle. The repository does not cite an exact passage or decide which reading is
intended.

The corpus also contains distinct overlapping targets: `THM-M-1381` (Maupertuis principle),
`THM-M-1518` (the same Chinese title and gloss in mathematical physics), `THM-P-0748` (an extremal
action formulation), and `THM-P-0749` (Euler-Lagrange as a necessary condition). Their records and
artifacts are discovery inputs only. No statement or proof credit is transferred between IDs.

This intake therefore freezes the ambiguity rather than inventing a theorem. The provisional root
vector is `[H5, M4, R4]`. Here `H5` says that the catalog wording is not yet a stable proposition;
it does not say that correctly stated stationary-action theorems are false or open. A narrow pinned
Lean probe checks only adjacent calculus and interval-integral APIs. No canonical Lean expression,
H0, M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
