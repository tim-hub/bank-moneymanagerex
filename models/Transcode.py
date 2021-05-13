from enum import Enum


class Transcode(Enum):

    def __str__(self):
        return str(self.value)

    Withdraw = 'Withdraw'
    Deposit = 'Deposit'
    Transfer = 'Transfer'
    Unknown = 'Unknown'

