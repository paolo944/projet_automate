# -*- coding: utf-8 -*-
"""
Code modifiable.
"""

from automate import Automate
from state import State
from transition import Transition
from myparser import *

"""automate = Automate.creationAutomate("exempleAutomate.txt")
automate.show("exempleAutomate")

s1= State(1, False, False)
s2= State(2, False, False)
print (s1==s2)
print (s1!=s2)"""

#2 Prise en main

#2.1:

#Etats:
s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, False, True)

#Transitions:
t1 = Transition(s0, "a", s0)
t2 = Transition(s0, "b", s1)
t3 = Transition(s1, "a", s2)
t4 = Transition(s1, "b", s2)
t5 = Transition(s2, "a", s0)
t6 = Transition(s2, "b", s1)

#Automate:
auto = Automate([t1, t2, t3, t4, t5, t6])
auto1 = Automate([t1, t2, t3, t4, t5, t6], [s0, s1, s2])
auto2 = Automate.creationAutomate("auto.txt")

#print(auto)
#print("\n")
#print(auto1)
#print("\n")
#print(auto2)
#auto.show("./automate/A_ListeTrans")
#auto1.show("./automate/A_ListeTrans1")
#auto2.show("./automate/A_ListeTrans2")

#2.2:

t = Transition(s0, "a", s1)
#print(auto.removeTransition(t1))
#print(auto.addTransition(t1))
#print(auto)

#print(auto.removeState(s1))
#print(auto.addState(s1))

s2 = State(0, True, False)
#print(auto.addState(s2))

#print(auto1.getListTransitionsFrom(s1))

#TEST Partie 3:

#Test succ:
#print(auto.succ([s0, s1, s2], "a"))

#Test accept:
#print(Automate.accepte(auto, "aabbb"))

#Test estComplet:

#print(Automate.estComplet(auto, "abc"))
t7 = Transition(s0, "a", s1)
#auto.addTransition(t7)
#print(auto)
#print(Automate.estDeterministe(auto))

#Test completion
#compAuto = Automate.completeAutomate(auto, "abc")
#print(compAuto)
#print(Automate.estComplet(compAuto, "abc"))

#Test determinisation
s0prime = State(0, True, False)
s1prime = State(1, False, False)
s2prime = State(2, False, False)
s3prime = State(3, False, True)
t1prime = Transition(s0prime, "a", s0prime)
t2prime = Transition(s0prime, "b", s0prime)
t3prime = Transition(s0prime, "a", s1prime)
t4prime = Transition(s1prime, "b", s2prime)
t5prime = Transition(s2prime, "a", s3prime)

autoprime = Automate([t1prime, t2prime, t3prime, t4prime, t5prime], [s0prime, s1prime, s2prime, s3prime])

print(Automate.determinisation(autoprime))