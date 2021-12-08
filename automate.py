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
    def determinisation(auto):
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        if Automate.estDeterministe(auto):
            return auto
        else:
            """initialStatesDet = []
            listTransitionsDet = []
            transitions = auto.listTransitions
            statesDet = []
            alphabet = auto.getAlphabetFromTransitions()
            finalStatesDet = []
            initialStates = auto.getListInitialStates()
            states = auto.listStates"""
            # On crée l'état initial et l'ajoute à l'automate résultat
            compteID = 0
            listeInit = auto.getListInitialStates()
            initialState: State = State(compteID, True, False, str(listeInit))

            # L'état initial est aussi final si un de ses états l'est
            for etat in listeInit:
                if etat.fin:
                    initialState.fin = True
                    break

            # On crée l'automate résultat avec notre état initial
            autoRes = Automate(listStates=[initialState], listTransitions=[], label="")

            # On récupère l'alphabet de l'automate
            alphabet = auto.getAlphabetFromTransitions()

            # On crée notre dico ID de l'ensemble d'états : liste des états contenus dans notre ensemble d'états
            dicoListe = {0: listeInit}

            # Ensemble des états dont on doit calculer les transitions crées
            aTraiterEns = {initialState}
            # Ensemble des états déjà vu, donc à ne pas recalculer
            deja_vu = set()
            # Pour stocker tous les nouveaux états à calculer
            tempEtats = set()
            # Un état temp pour nos calculs
            etatTemp: State = initialState

            while aTraiterEns != set():
                # Tant qu'on a des nouveaux états à traiter
                for aTraiterEtat in aTraiterEns:
                    for lettre in alphabet:
                        listeSucc = auto.succElem(dicoListe[aTraiterEtat.id], lettre)
                        # Liste des successeurs

                        labelEtat = str(listeSucc)  # Calcul du label de l'état

                        for etat in autoRes.listStates:
                            # On regarde si l'état avec le label correspondant existe déjà
                            if etat.label == labelEtat:
                                etatTemp = etat
                                break
                        if etatTemp.label != labelEtat:
                            # Si le label ne match pas, c'est qu'on n'a pas trouvé d'état correspondant
                            compteID += 1
                            # On incrémente l'ID et crée l'état
                            etatTemp: State = State(compteID, False, False, str(listeSucc))
                            dicoListe[compteID] = listeSucc
                            # On stocke la liste des états correspondants à l'ID dans notre dictionnaire
                            for etat in listeSucc:
                                # On rend l'état final s'il contient au moins un état final
                                if etat.fin:
                                    etatTemp.fin = True
                                    break

                        autoRes.addTransition(Transition(aTraiterEtat, lettre, etatTemp))
                        # On crée la transition de l'état aTraiter à l'état suivant
                        tempEtats.add(etatTemp)
                        # On ajoute le nouvel état à notre ensemble des successeurs à calculer

                deja_vu = deja_vu | aTraiterEns
                # Les ensembles qu'on a traité deviennent déjà vu
                aTraiterEns = tempEtats - deja_vu
                # Les prochains états à calculer sont les successeurs
                # moins ceux déjà visités
                tempEtats = set()

            return autoRes

    @staticmethod
    def complementaire(auto, alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        autoComplet = auto
        if not Automate.estComplet(autoComplet, alphabet):
            autoComplet = Automate.completeAutomate(auto, alphabet)
        if not Automate.estDeterministe(auto):
            autoComplet = Automate.determinisation(autoComplet)
        for state in autoComplet.listStates:
            if state.fin:
                state.fin = False
            else:
                state.fin = True
        return autoComplet

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
