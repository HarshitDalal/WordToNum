from utility import GetLanguage


class WordToNumber:
    def __init__(self, lang="en"):
        self.word_to_num = GetLanguage().get_language(lang)[0]

    def convert(self, words):
        words = words.split()
        total, current, decimal_part, decimal_place = 0, 0, 0, 0.1
        is_decimal, is_negative = False, False

        for word in words:
            if word == "negative":
                is_negative = True
            elif word == "point":
                is_decimal = True
            elif word.isdigit():
                current, decimal_part, decimal_place = self.process_digit(word, is_decimal, current, decimal_part, decimal_place)
            elif word in self.word_to_num:
                current, total, decimal_part, decimal_place = self.process_word(word, is_decimal, current, total, decimal_part, decimal_place)
            else:
                raise ValueError(f"Word '{word}' is not recognized.")

        result = total + current + decimal_part
        if is_negative:
            result = -result
        return result

    def process_digit(self, word, is_decimal, current, decimal_part, decimal_place):
        scale = int(word)
        if is_decimal:
            decimal_part += scale * decimal_place
            decimal_place /= 10
        else:
            current += scale
        return current, decimal_part, decimal_place

    def process_word(self, word, is_decimal, current, total, decimal_part, decimal_place):
        scale = self.word_to_num[word]
        if is_decimal:
            decimal_part += scale * decimal_place
            decimal_place /= 10
        else:
            current, total = self.update_total_and_current(scale, current, total)
        return current, total, decimal_part, decimal_place

    def update_total_and_current(self, scale, current, total):
        if scale >= 1000:
            if current == 0:
                current = 1
            current *= scale
            total += current
            current = 0
        elif scale >= 100:
            current *= scale
        else:
            current += scale
        return current, total