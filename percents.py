def percents(x, y):
    """What persentage of x is y"""
    one_percent = x / 100
    result = y / one_percent
    print(str(y) + "is" + str(result) + "persent of" + str(x))

percents(200,50)