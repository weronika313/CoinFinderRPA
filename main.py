import rpa as r

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    r.init()
    r.url('https://www.metalmarket.eu/')
    r.click("//*[@id='ni_789']")
    r.click("//*[@id='ni_851']")
    r.click("//*[@class= 'btn show_filters visible-phone']")
    r.click("//*[@id= 'filter_traits1_val367']")
    r.click("//*[@id= 'filter_traits510_val481']")
    r.click("//*[@id= 'filters_submit']")


    r.snap('page', 'results.png')
    r.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
