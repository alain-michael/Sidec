def avg(iter, attr=None):
    if attr is None:
        total = sum(iter)
    else:
        total = sum(getattr(i, attr) for i in iter)
    return total/len(iter)