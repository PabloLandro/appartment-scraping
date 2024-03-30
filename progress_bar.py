import time

class Progress_bar:
    def __init__(self, width=40, start_time=time.time(), total=0, index=0):
        self.width = width
        self.start_time = start_time
        self.index = 0
        self.total = total

    def _get_text(self):
        hours, remainder = divmod(self.estimated_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        progress = int((self.index) / self.total * self.width)
        bar = '[' + '#' * progress + ' ' * (self.width - progress) + ']'
        elapsed_time_formatted = "estimated time {:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        return f'\r{bar} {self.index}/{self.total} apartments screaped. {elapsed_time_formatted}'

    def _update(self):
        self.index += 1
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        mean_time = elapsed_time / self.index
        self.estimated_time = mean_time * (self.total-self.index)
        

    def increment(self, do_print=True):
        self._update()
        if do_print:
            print(self._get_text(), end='', flush=True)
        else:
            return self.get_text()