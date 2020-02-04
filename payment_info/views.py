from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):

    def vars_for_template(self):
        participant = self.participant
        return {
            'redemption_code': participant.label or participant.code,
        }

    timeout_seconds = 400

    def is_displayed(self):
        return self.round_number == 8

page_sequence = [PaymentInfo]
