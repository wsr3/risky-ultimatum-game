from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from . import models
from .models import Constants


class Consent(Page):
    form_model = models.Player
    form_fields = ['consent_name', 'consent_date']

    def is_displayed(self):
        return self.round_number == 1


class Introduction(Page):
    timeout_seconds = 300

    def vars_for_template(self):
        return {
            'is_proposer': True if self.participant.vars['type'] == 'proposer' else False,
        }

    def is_displayed(self):
        return self.round_number == 1


class OfferR1(Page):
    form_model = models.Player
    form_fields = ['amount_offered', 'pMAO']

    def is_displayed(self):
        return self.player.participant.vars['type'] == 'proposer' and self.round_number == 1

    timeout_seconds = 300


class Offer(Page):
    form_model = models.Player
    form_fields = ['amount_offered']

    def is_displayed(self):
        return self.player.participant.vars['type'] == 'proposer' and self.round_number >= 2
    timeout_seconds = 300

    # lottery
    def vars_for_template(self):
        return {
            'win_pct': "{0:.0%}".format(Constants.win_prob[self.round_number - 3]),
            'win_num': int(Constants.win_prob[self.round_number - 3] * 10),
        }


class FWaitPageProposer(Page):
    template_name = 'ultimatum/FWaitPage.html'
    timeout_seconds = 120

    def is_displayed(self):
        return self.player.participant.vars['type'] == 'proposer' and self.round_number >= 2


class FWaitPageResponder(Page):
    template_name = 'ultimatum/FWaitPage.html'
    timeout_seconds = 120

    def is_displayed(self):
        return self.player.participant.vars['type'] == 'responder' and self.round_number >= 2


class AcceptStrategyR1(Page):
    form_model = models.Player
    form_fields = ['min_accepted']

    def is_displayed(self):
        return self.player.participant.vars['type'] == 'responder' and self.round_number == 2

    timeout_seconds = 300


class AcceptStrategy(Page):
    form_model = models.Player
    form_fields = ['min_accepted', 'responder_offered']

    def is_displayed(self):
        return self.player.participant.vars['type'] == 'responder' and self.round_number > 2

    # lottery
    def vars_for_template(self):
        return {
            'win_pct': "{0:.0%}".format(Constants.win_prob[self.round_number - 3]),
            'win_num': int(Constants.win_prob[self.round_number - 3] * 10),
            'responder_round': self.round_number - 1
        }
    timeout_seconds = 300


class Survey(Page):
    form_model = models.Player
    form_fields = ['q_age',
                   'q_gender',
                   'q_education',
                   'q_income',
                   'q_gamble',
                   'q_fair',
                   'q_risk']

    def is_displayed(self):
        return self.round_number == 8
    timeout_seconds = 300


class ResultsFinal(Page):

    def is_displayed(self):
        return self.round_number == 8

    timeout_seconds = 300

    def vars_for_template(self):
        return {
            'is_proposer': True if self.participant.vars['type'] == 'proposer' else False,
        }

page_sequence = [Consent,
                 Introduction,
                 OfferR1,
                 Offer,
                 FWaitPageProposer,
                 AcceptStrategyR1,
                 AcceptStrategy,
                 FWaitPageResponder,
                 Survey,
                 ResultsFinal]
