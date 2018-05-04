# -*- coding: utf-8 -*-
import pandas as pd
from .models import restaurant
from django.utils import timezone

import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

restaurant_df = pd.read_csv('anniversary/restaurant.csv')

col = restaurant_df.columns.tolist()

for i,r in restaurant_df.iterrows():
    res = restaurant(name = unicode(r[col[0]],'euc-kr'), restaurant_type = unicode(r[col[1]],'euc-kr'),
                        url = unicode(r[col[2]],'euc-kr'),phonenumber = unicode(r[col[3]],'euc-kr'),
                        desc = unicode(r[col[4]],'euc-kr'), date = timezone.now())

    try:
        res.save()
    except:
        # if the're a problem anywhere, you wanna know about it
        print "there was a problem with line", i
