class Observable(object):
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)


class Observer(object):
    def __init__(self):
        self.__observables = []
        self.mute = False

    def notify(self, observable, *args, **kwargs):
        if not self.mute:
            print args


if __name__ == '__main__':
    subject = Observable()
    observer = Observer(subject)
    subject.notify_observers("HELLO WORLD")