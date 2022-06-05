import os

class Speaker():
    def __init__(self):
        self.State = dict(
            volume = 80,
        )

        self.Commands = dict(
            volumeUpdate = 'amixer set Master {volume}%',
        )

    def setVolume(self, vol):
        self.__setState(dict(
            volume = vol,
        ))
    
    def __setState(self, state):
        for key, val in state.items():
            self.State[key] = val

        os.system(self.Commands['volumeUpdate'].format(volume = self.State['volume']))


def main():
    spk = Speaker()
    for i in range(0, 101):
        spk.setVolume(90)

if __name__=='__main__':
    main()