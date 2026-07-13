# THM-M-0099 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named "Ngo Bao
Chau theorem." The repository attributes it to Ngo Bao Chau in 2008 and gives only the gloss
"proof of the Fundamental Lemma." The catalog's `verified` label is untrusted inventory metadata,
not an exact source statement, a Lean theorem, or proof evidence.

The gloss identifies Ngo's Lie-algebra Fundamental Lemma proof family. The inspected source lead is
Ngo's 2008 arXiv v3 manuscript, later published as *Le lemme fondamental pour les algebres de Lie*,
PMIHES 111 (2010), 1-169. Its introduction states the normalized equality between a kappa-orbital
integral and a stable endoscopic orbital integral; the detailed local statement is Theorem 1.11.1.
The paper proves the equal-characteristic case and cites Waldspurger for the unequal-characteristic
transfer.

That source lead does not yet freeze this target's canonical claim. The repository contains a
second target, `THM-M-0434`, with the same author, year, and gloss, and its legacy Lean file and
rev-5.6 dossier are not transferable proof or scope evidence. Accountable review must decide whether
the two catalog IDs are duplicates, assign source ownership, choose the introductory or detailed
source formulation with every incorporated definition, and audit the characteristic-transfer
boundary. No such accepted decision exists at intake.

Pinned mathlib provides local-field, scheme, and Haar-measure infrastructure. `IntakeProbe.lean`
authenticates three adjacent APIs, but the bounded search found no endoscopy, transfer-factor, or
orbital-integral target. The separate legacy `S1_M_083.lean` uses abstract surrogate data and is
only a discovery boundary for `THM-M-0434`; it is neither imported nor credited here.

The provisional vector is `[H1, M4, R4]`: a complete published proof source lead is known, but its
exact statement and duplicate-ID ownership are not accepted; no usable exact formal artifact is
credited; and no source-faithful readable reconstruction exists. All six downstream phases remain
open. No H0, M0, R0, accepted state, audit completion, theorem completion, or master acceptance is
claimed.
