from feapder.pipelines import BasePipeline
from typing import Dict, List, Tuple
from feapder.utils.log import log


class Pipeline(BasePipeline):
    """
    xx pipeline
    """

    def save_items(self, table, items: List[Dict]) -> bool:
        """
        Save data to Wordpress
        """
        for item in items:
            try:
                title = item['title']

                log.debug(f'Submit article: {title}')

                item['translations'] = []

                self.post_article(item)

            except Exception as e:
                log.error(f'Rewrite and translate error: {e}')

        print("Custom_Pipeline, save item >>>>", table, len(items), 'items')

        return True

    def post_article(self, item):
        """Post an article to API"""
        pass
