from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Stage1(Page):

    form_model = 'group'
    form_fields = ['r', 'checkr', 'historyc1']

    def error_message(self, value):
        #if self.group.r == None:
            if value["checkr"] == None:
                return 'Please make a decision using slider'

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return{
            'e': float(self.group.e_g),
            'round_number_perc': self.subsession.round_number/Constants.num_rounds * 100,
        }

    def before_next_page(self):
        self.player.historyc = self.group.historyc1

class WaitForP1(WaitPage):
    pass

class Stage2(Page):

    form_model = 'group'
    form_fields = ['payoff1f', 'checkpayoff1f', 'historyc2']

    def error_message(self, value):
        if self.group.r < 1:
            if value["checkpayoff1f"] == None:
                return 'Please make a decision using slider'

    def vars_for_template(self):
        return{
            'e': float(self.group.e_g),
            'r': self.group.r,
            'r_i2': 1.00 - self.group.r,
            'r_i': round(1.00 - self.group.r, 2),
            'rpayoff1': self.group.r*(15-float(self.group.e_g)),
            'rpayoff2': self.group.r*5,
            'round_number_perc': self.subsession.round_number / Constants.num_rounds * 100
        }

    def is_displayed(self):
        return self.player.id_in_group == 2

    def before_next_page(self):
        self.player.historyc = self.group.historyc2

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.calculate_payoff1()
        self.group.calculate_payoff2()
        self.group.calculate_payoff_p1_p2()
        self.group.set_payoffs()

class Results(Page):

    form_model = 'group'
    form_fields = ['historyr1', 'historyr2']

    def before_next_page(self):
        self.player.historyr = self.group.historyr1
        self.player.historyr = self.group.historyr2

    def vars_for_template(self):
            return {
                'round_number_perc': self.subsession.round_number / Constants.num_rounds * 100
            }

class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number != Constants.num_rounds

page_sequence = [
    Warning,
    Stage1,
    WaitForP1,
    Stage2,
    ResultsWaitPage,
    Results,
    ShuffleWaitPage
]
