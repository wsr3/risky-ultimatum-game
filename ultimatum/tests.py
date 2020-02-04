from otree.api import Currency as c, currency_range, Submission
from . import views
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.group.round_number == 1:
            yield(views.Consent, {'consent_name': 'test',
                                  'consent_date': '05/31/2017'})
            yield (views.Introduction)

        if self.player.participant.vars['type'] == 'proposer':
            if self.player.round_number == 1:
                yield (views.OfferR1, {'amount_offered': c(random.randrange(0, 100, 5)),
                                       'pMAO': c(random.randrange(0, 100, 5))})
            else:
                yield (views.Offer, {'amount_offered': c(random.randrange(0, 100, 5))})
                yield Submission(views.FakeWaitPageProposer, check_html=False)
        else:
            if self.player.round_number == 2:
                yield (views.AcceptStrategyR1, {'min_accepted': c(random.randrange(0, 100, 5))})
                yield Submission(views.FakeWaitPageResponder, check_html=False)
            elif self.player.round_number >= 3:
                yield (views.AcceptStrategy, {'min_accepted': c(random.randrange(0, 100, 5)),
                                              'responder_offered': c(random.randrange(0, 100, 5))})
                yield Submission(views.FakeWaitPageResponder, check_html=False)

        if self.player.round_number == 8:
            yield (views.Survey, {'q_gender': 'Male',
                                  'q_age': '20',
                                  'q_education': 'High school',
                                  'q_income': 50000,
                                  'q_gamble': '50% chance of winning $10 and 50% chance of winning $10',
                                  'q_fair': 'Compared to other people, I\'m much more intolerant to being unfairly treated.',
                                  'q_risk': 'I\'m much more risk loving than other people'})
            yield (views.ResultsFinal)



