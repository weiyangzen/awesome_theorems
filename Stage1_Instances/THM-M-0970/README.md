# THM-M-0970 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item named the
Moser-Tardos algorithm. The repository supplies only the gloss "a constructive proof of the Lovasz
Local Lemma," attributes it to Robin Moser and Gabor Tardos in 2010, and labels it verified. That
label is untrusted inventory metadata, not an exact proposition, source review, or machine proof.

The archived author paper *A constructive proof of the general Lovasz Local Lemma* identifies the
natural theorem family. Its Theorem 1.2 analyzes Algorithm 1.1 for finitely many mutually independent
random variables and finitely many bad events determined by them. Under the asymmetric local-lemma
product criterion, the algorithm repeatedly chooses an arbitrary violated event and independently
resamples its determining variables. The paper proves an expected resampling bound for each event
and for the total execution. This is a strong candidate source root, but the catalog does not cite
the paper or select Theorem 1.2 rather than its existential, parallel, deterministic, or lopsided
variants. No independent reviewer has accepted the source mapping, so intake does not silently make
that proposition canonical.

Pinned mathlib supplies probability spaces, indexed independence, product measures, probability
mass functions, and expectation infrastructure. `IntakeProbe.lean` authenticates a narrow set of
those interfaces. A bounded exact-topic search found no Moser-Tardos, algorithmic local-lemma, witness
tree, or bad-event resampling declaration in pinned mathlib or repo-local Lean. The adjacent APIs do
not define Algorithm 1.1 and receive no target or proof credit.

The provisional vector is `[H1, M4, R4]`: a complete primary proof source and natural candidate root
are known, but exact source adoption, clause mapping, correction review, and independent approval
remain open; no usable exact formal artifact has been located; and no source-faithful proof
reconstruction is available. `instance.json` is the structured scope authority and `task-dag.json`
keeps all six downstream phases open. No exact statement, H0, M0, R0, accepted proof state, audit
completion, theorem completion, accepted receipt, or master acceptance is claimed.
