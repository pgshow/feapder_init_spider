"""
----------
Database control for postgresql
---------
"""

from feapder import Item


class PgSpiderDataItem(Item):
    __unique_key__ = ["url"]  # duplicate key

    def __init__(self, *args, **kwargs):
        self.url = None

    def pre_to_db(self):
        """Convert the python data to postgresql valid data"""
        try:
            # self.row_name = self.str2char_var(self.row_name)
            pass
        except:
            pass

    @staticmethod
    def list_text(var):
        """python list to []text"""
        if not var or not isinstance(var, list):
            return None

        return '{"' + '","'.join(var) + '"}'

    @staticmethod
    def boolean(var):
        """python bool to postgres boolean"""
        if not var or not isinstance(var, bool):
            return "false"
        else:
            return "true"

    @staticmethod
    def str2char_var(var):
        """python string to postgres character varying"""
        if not var or not isinstance(var, str):
            return None
        else:
            return f"{var}"

    @staticmethod
    def list2list_text(var):
        """python list to postgres []text"""
        return None
