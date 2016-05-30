from data_reader import DataReader
from model.signal import Signal
from helper.attribute_helper import AttributeHelper

SINGALS = '../data/signal_sample.csv'


class SignalReader(DataReader):

    def __init__(self, filename=SINGALS):
        super(SignalReader, self).__init__(filename)

        self._signals = None

    @property
    def signals(self):
        if self._signals is None:
            self._signals = []
            for row in self:
                self._signals.append(AttributeHelper.assign_attribute(Signal(), row))
        return self._signals

if __name__ == "__main__":
    reader = SignalReader()

    import pprint
    pprint.pprint(reader.signals)