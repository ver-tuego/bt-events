import re
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def cmd(point, rating, day):
    x = []
    y = []

    fig, ax = plt.subplots()
    fig.set_figwidth(12)
    fig.set_figheight(6)
    ax.grid(linestyle = '--',
            color = '#bfbfbf')
    fig.suptitle('@bt-events', fontsize = 18)

    y.append(rating)
    res = point.split('_'); res.pop();
    res.reverse()

    for i in range(day+1):
        x.append((datetime.now() + timedelta(days=i)).strftime("%d.%m"))
        if i == day:
            pass
        else:
            y.append(rating - int(res[i]))
            rating = rating - int(res[i])
    y.reverse(); x.reverse()

    plt.scatter(x, y)
    plt.plot(x, y)
    plt.savefig('result.png')
    return 1
