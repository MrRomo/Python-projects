import time
from progress.bar import Bar

t = 1

bar = Bar('Processing', max=20)
for i in range(20):
    # Do some work
    print('\nprogress {}'.format(i))
    time.sleep(t)
    bar.next()
bar.finish()