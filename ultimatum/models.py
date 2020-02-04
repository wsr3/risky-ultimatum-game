from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import numpy as np
import random
import itertools


doc = """
Risky Ultimatum Game with 8 rounds using the Strategy Method. Players will be reshuffled between rounds and see the
final results.
"""


class Constants(BaseConstants):
    name_in_url = 'ultimatum'
    players_per_group = None
    num_rounds = 8
    win_prob = [0.5, 0.3, 0.9, 0.1, 0.7, 1]

    instructions_template = 'ultimatum/Instructions.html'

    endowment = c(100)
    payoff_if_rejected = c(0)
    offer_increment = c(5)

    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)


class Subsession(BaseSubsession):
    type = models.CharField()

    def before_session_starts(self):
        if self.round_number == 1:
            players = self.get_players()
            treat = itertools.cycle(['proposer', 'responder'])
            for p in players:
                p.participant.vars['type'] = next(treat)

        # initialize group variables
        for p in self.get_players():
            if np.random.binomial(1, Constants.win_prob[self.round_number - 3]) == 1\
                    and 3 <= self.round_number <= 8:
                p.won_lottery = True
            else:
                p.won_lottery = False  # False for round 1 and 2


class Group(BaseGroup):
    pass

    # payoff will be calculated manually
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        if self.round_number == 1:  # dictator game in round 1
            self.offer_accepted = 1
            p1.payoff = Constants.endowment - self.amount_offered
            p2.payoff = self.amount_offered
        else:  # round 2 to 8
            if self.strategy:
                self.offer_accepted = self.amount_offered >= self.min_accepted
            if self.round_number == 3:  # not payed in round 3
                p1.payoff = Constants.payoff_if_rejected
                p2.payoff = Constants.payoff_if_rejected

            if self.offer_accepted:  # accepted offer
                p1.payoff = Constants.endowment - self.amount_offered
                p2.payoff = self.amount_offered
            elif self.won_lottery and self.round_number >= 4:  # with lottery for round 4 to 8
                p1.payoff = self.responder_offered
                p2.payoff = Constants.endowment - self.responder_offered
            else:  # lose lottery for round 4 to 8
                p1.payoff = Constants.payoff_if_rejected
                p2.payoff = Constants.payoff_if_rejected


class Player(BasePlayer):
    consent_name = models.CharField()
    consent_date = models.CharField()
    amount_offered = models.CurrencyField(choices=Constants.offer_choices)
    min_accepted = models.CurrencyField(choices=Constants.offer_choices)
    responder_offered = models.CurrencyField(choices=Constants.offer_choices)
    offer_accepted = models.BooleanField(initial=True)
    won_lottery = models.BooleanField()
    pMAO = models.CurrencyField(choices=Constants.offer_choices)
    q_gender = models.CharField(initial=None,
                                choices=['Male', 'Female', 'Other', 'Prefer not to answer'],
                                verbose_name='What is your gender?',
                                widget=widgets.RadioSelect())
    q_age = models.PositiveIntegerField(verbose_name='What is your age?',
                                        choices=range(18, 100),
                                        initial=None)
    q_education = models.CharField(initial=None,
                                   choices=['Below high school', 'High school', 'College',
                                            'Graduate school', 'Prefer not to answer'],
                                   verbose_name='What is your educational attainment?',
                                   widget=widgets.RadioSelect())
    q_income = models.CharField(verbose_name='What is your annual household income?',
                                initial=None)
    q_gamble = models.CharField(initial=None,
                                choices=['50% chance of winning $10 and 50% chance of winning $10',
                                         '50% chance of winning $18 and 50% chance of winning $6',
                                         '50% chance of winning $26 and 50% chance of winning $2',
                                         '50% chance of winning $34 and 50% chance of losing $2',
                                         '50% chance of winning $42 and 50% chance of losing $6'],
                                verbose_name='If your were to play one of the following gamble, '
                                             'which one would you choose?',
                                widget=widgets.RadioSelect())
    q_fair = models.CharField(initial=None,
                              choices=['Compared to other people, I\'m much more intolerant to being unfairly treated.',
                                       'Compared to other people, I\'m a little more intolerant to being unfairly treated.',
                                       'I\'m as intolerant as other people in general to being unfairly treated.',
                                       'Compared to other people, I\'m a little less intolerant to being unfairly treated.',
                                       'Compared to other people, I\'m much less intolerant to being unfairly treated.',],
                              verbose_name='Which of the following statements do you agree?',
                              widget=widgets.RadioSelect())
    q_risk = models.CharField(initial=None,
                              choices=['I\'m much more risk loving than other people',
                                       'I\'m a little more risk loving than other people',
                                       'I\'m not different from other people in general in terms of risk attitude',
                                       'I\'m a little less risk loving than other people',
                                       'I\'m much less risk loving than other people',],
                              verbose_name='Which of the following statements do you agree?',
                              widget=widgets.RadioSelect())
