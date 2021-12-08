# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from itertools import product
from automateBase import AutomateBase


class Automate(AutomateBase):

    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs

    def succ(self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        listeStateRetour = []
        for s in listStates:
            for i in self.succElem(s, lettre):
                if i not in listeStateRetour:
                    listeStateRetour += i
        return listeStateRetour

    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """

    @staticmethod
    def accepte(auto, mot):
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        mot_manip = mot
        listFinalStates = auto.getListFinalStates()
        listStatesFin = auto.getListInitialStates()
        for lettre in mot_manip:
            listStatesFin = auto.succ(listStatesFin, lettre)
        for state in listStatesFin:
            if (state in listFinalStates):
                return True
        return False

    @staticmethod
    def estComplet(auto, alphabet):
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """
        listStates = auto.listStates
        for state in listStates:
            for lettre in alphabet:
                if (auto.succElem(state, lettre) == []):
                    return False
        return True

    @staticmethod
    def estDeterministe(auto):
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        listStates = auto.listStates
        if len(auto.getListInitialStates()) > 1:
            return False
        else:
            listStates = auto.listStates
            etiquettes = auto.getAlphabetFromTransitions()
            for state in listStates:
                for etiquette in etiquettes:
                    if len(auto.succElem(state, etiquette)) > 1:
                        return False
            return True

    @staticmethod
    def completeAutomate(auto, alphabet):
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        if Automate.estComplet(auto, alphabet):
            return auto
        else:
            autocomplet = copy.deepcopy(auto)
            listStates = auto.listStates
            sn = State(len(listStates), False, False)
            for state in listStates:
                for lettre in alphabet:
                    if auto.succElem(state, lettre) == []:
                        autocomplet.addTransition(Transition(state, lettre, sn))
                    autocomplet.addTransition(Transition(sn, lettre, sn))
        return autocomplet

    @staticmethod
    def parties(ensemble):
        """Liste -> Liste(Parties de l'ensemble)
        rend la liste des parties de l'ensemble donné
        """
        if len(ensemble) == 1:
            return [ensemble]
        else:
            p = Automate.parties(ensemble[1:])
        return p + [[ensemble[0]] + partie for partie in p]

    @staticmethod
    def determinisation(auto):
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        if Automate.estDeterministe(auto):
            return auto
        else:
            initialStatesDet = []
            listTransitionsDet = []
            transitions = auto.listTransitions
            statesDet = []
            alphabet = auto.getAlphabetFromTransitions()
            finalStatesDet = []
            initialStates = auto.getListInitialStates()
            states = auto.listStates
            for s in initialStates:
                initialStatesDet.append(s)
            initialStatesDet = State(set(initialStatesDet), True, False)
            ListParties = Automate.parties(auto.listStates)
            parties = set[State]
            for i in ListParties:
                print(i)

            for x in parties:
                for a in alphabet:
                    for sprime in states:
                        for s in x:
                            if Transition(s, a, sprime) in transitions:
                                if x not in statesDet:
                                    statesDet.append(x)
            return statesDet

    @staticmethod
    def complementaire(auto, alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """

    @staticmethod
    def intersection(auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        return

    @staticmethod
    def union(auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        return

    @staticmethod
    def concatenation(auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        return

    @staticmethod
    def etoile(auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        return
