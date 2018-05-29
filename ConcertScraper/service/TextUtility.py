class TextUtility:
    @staticmethod
    def find_in_text(text, keywords):
        for keyword in keywords:
            if text.lower().find(keyword) >= 0:
                return text.lower().find(keyword)
        return -1
