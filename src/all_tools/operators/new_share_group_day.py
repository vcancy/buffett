import pandas as pd

from src.base import Operator
from src.constant import data_type
from src.parse.df import add_col_by_group_sum, add_col_by_group_undefined
from src.register import require, register


@require(data_type.new_share_total)
@register
class NewShareOp(Operator):
    data_type = data_type.new_share_group_day
    data_suffix = "csv"

    def __init__(self, start_date, end_date):
        super().__init__(start_date, end_date)
        self.load_require()

    def get_data(self):
        df = self.new_share_total.get_ret()
        return df

    def run1(self):
        df = self.get_data()
        df = add_col_by_group_sum(df, "ipo_date", "total_price", "market_total_price")
        return df

    def run(self):
        df = self.get_data()

        def my_agg(x):
            names = {
                'total_price': x['total_price'].sum(),
                'market_total_price': x['market_total_price'].sum(),
                'day_count': x['name'].count()
            }

            return pd.Series(names)

        df = add_col_by_group_undefined(df, "ipo_date", my_agg)
        return df
