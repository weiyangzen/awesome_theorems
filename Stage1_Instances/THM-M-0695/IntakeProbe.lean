import Mathlib

#check Prop
#check And
#check Or
#check Exists
#check False
#check @And.intro
#check @And.elim
#check @Or.elim
#check @Exists.intro
#check fun {P Q : Prop} (f : P → Q) (p : P) => f p
#check fun {P Q : Prop} (p : P) (q : Q) => And.intro p q
