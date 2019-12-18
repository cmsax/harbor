
class Marshaller:
    """Class for marshalling weibo json object.
    """
    mobile_card_types = {
        9: 'post', 31: 'search-box'
    }
    mobile_card_keys = [
        'attitudes_count', 'pics', 'pic_num', 'id', 'created_at',
        'comments_count', 'favorited', 'reads_count', 'reposts_count',
        'source', 'text', 'textLength', 'visible', 'weibo_position',
        ['title', 'text']
    ]
    @classmethod
    def mobile_card(cls, card_object):
        """Extract main content from weibo h5 json card.

        Args:
            card_object: (dict) card item from weibo api

        Returns:
            ({str: object} or None)
        """
        if cls.mobile_card_types.get(card_object['card_type'], None) != 'post':
            return None
        result = {}
        card = card_object['mblog']
        for key in cls.mobile_card_keys:
            if isinstance(key, str):
                try:
                    result[key] = card[key]
                except Exception as e:
                    print(e, str(e))
                    pass
            else:
                tmp = card
                for sub_key in key:
                    tmp = tmp[sub_key]
                result['.'.join(key)] = tmp

        return result
