# THM-M-0761 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository target `泵引理`
("pumping lemma"). The complete target gloss is `正则语言与上下文无关语言的泵引理`: the
pumping lemmas for regular and context-free languages. Repository computer-science records confirm
that this wording intentionally names two distinct theorem families rather than one unspecified
use of the singular title.

The usual regular-language lemma decomposes a sufficiently long word into three factors with one
nonempty iterated factor lying within a bounded initial segment. The context-free-language lemma instead uses
five factors, pumps two factors together, and imposes different length and nonemptiness conditions.
The catalog supplies neither formula, pumping-length convention, language representation, nor an
authoritative source passage. Selecting only one lemma, or treating the two as interchangeable,
would silently substitute or weaken the scheduled collective target.

A bounded probe against pinned mathlib confirms that it provides languages, finite-state automata,
`Language.IsRegular`, `DFA.pumping_lemma`, context-free grammars, and
`Language.IsContextFree`. The pinned DFA theorem is a proof-bearing discovery lead for one branch;
the context-free grammar module exposes no pumping theorem under an obvious name. These facts are
feasibility observations only. They do not freeze the collective canonical target, transfer proof
credit, or constitute the later anchor audit.

The provisional root vector is `[H1, M4, R4]`: both standard theorem families have a historical
primary-source bibliographic lead, but exact source text, assumptions, proof mapping, errata, and
independent review remain open; no collective Lean expression or readable reconstruction is
accepted. The lifecycle remains `planned`, every downstream task is open, and no proof state,
audit completion, theorem completion, or master acceptance is claimed.
