# THM-M-0071 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0071`, the classification of
finite simple groups. The catalog supplies the literal claim that every finite simple group belongs
to 18 infinite families or 26 sporadic groups, a collective attribution, the year 1983, and an
untrusted `partially verified` label. It supplies no citation, definitions, family roster,
parameters, exceptions, isomorphism convention, quantified proposition, or proof boundary.

The wording identifies the classification theorem but is not binder- or taxonomy-complete. In
particular, it does not say which convention counts the cyclic prime-order and alternating families
together with 16 Lie-type families as 18, how low-rank coincidences and nonsimple parameters are
removed, how the Tits group is treated, or whether the conclusion asserts only exhaustiveness or
also uniqueness and nonisomorphism. Inventing predicates named after those families would hide the
mathematics rather than transcribe it.

Valdo Tatitscheff's expository arXiv preprint *A short introduction to Monstrous Moonshine*, version
4, was inspected as an exact-wording witness: its Theorem 1 states the same 18-infinite-family or
26-sporadic alternative and explains the 18-family count. It is a secondary statement witness, not
a primary proof source, catalog provenance, or `H0` evidence. Daniel Gorenstein's 1983 book *The
Classification of Finite Simple Groups*, Volume 1, was also inspected as a primary-book source
lead matching the catalog year. Its publisher material describes the full classification as a
30-year, roughly 500-article proof, but the volume itself treats groups of noncharacteristic 2 type
and reduces a minimal counterexample to characteristic 2 type. Thus it supports the theorem-family
and proof-boundary crosswalk, not a complete primary-source proof ledger. The catalog cites neither
source.

`instance.json` freezes the provisional vector `[H1, M4, R4]`: the established published theorem
family is identifiable, while exact statement/source mapping remains open; no source-identical
formal root is located; and no complete source-to-proof reconstruction exists. `IntakeProbe.lean`
elaborates only pinned simple-group infrastructure, the finite abelian-simple classification, and
the simplicity of `A5`. These are real adjacent branches but receive no root or coverage credit.
All six downstream tasks remain open in `task-dag.json`.

No canonical mathematical or Lean statement, H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
