# THM-M-0743 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the recursion-theory catalog item
`不动点定理` (fixed-point theorem). The repository attributes it to Stephen Kleene in 1938 and
supplies only the gloss `递归函数的不动点` ("a fixed point of recursive functions"). Those fields
identify a theorem family, not a binder-complete proposition.

Pinned mathlib contains two unusually strong discovery candidates in
`Mathlib.Computability.PartrecCode`. `Nat.Partrec.Code.fixed_point` is documented there as Rogers'
fixed-point theorem: a total computable transformation of program codes has a code whose transformed
and original programs compute the same partial function. `Nat.Partrec.Code.fixed_point₂` is
documented as Kleene's second recursion theorem: a partial-recursive binary family has a program
whose evaluation is its own specialization. These are related, but they have different binders and
conclusions.

The catalog does not choose between them. Its neighboring `THM-M-0742` separately names the
recursion theorem and self-reference, while `THM-M-0744` separately names the s-m-n theorem. An
outside-scope computer-science record also equates Kleene's second recursion theorem with a
fixed-point gloss. Selecting one candidate here would therefore risk duplicating or substituting a
neighbor rather than preserving this target.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: the established theorem family and pinned candidates are known, but the exact source
variant and source-to-target ownership are unresolved; no candidate receives machine credit before
statement identity is frozen; and no reviewed reconstruction can attach to an unfrozen root. All six
downstream tasks remain open. Neither audit completion nor theorem completion is claimed.
