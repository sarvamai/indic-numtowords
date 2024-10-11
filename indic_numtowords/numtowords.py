import re
import csv

from indic_numtowords.asm.cardinal import convert as as_convert
from indic_numtowords.ben.cardinal import convert as bn_convert
from indic_numtowords.eng.cardinal import convert as en_convert
from indic_numtowords.guj.cardinal import convert as gu_convert
from indic_numtowords.hin.cardinal import convert as hi_convert
from indic_numtowords.mal.cardinal import convert as ml_convert
from indic_numtowords.mar.cardinal import convert as mr_convert
from indic_numtowords.ori.cardinal import convert as or_convert
from indic_numtowords.pun.cardinal import convert as pa_convert
from indic_numtowords.tam.cardinal import convert as ta_convert
from indic_numtowords.tel.cardinal import convert as te_convert
from indic_numtowords.kan.cardinal import convert as kn_convert
from indic_numtowords.urd.cardinal import convert as ur_convert

from indic_numtowords.asm.data.user_variations import variations as as_variations
from indic_numtowords.ben.data.user_variations import variations as bn_variations
from indic_numtowords.eng.data.user_variations import variations as en_variations
from indic_numtowords.guj.data.user_variations import variations as gu_variations
from indic_numtowords.hin.data.user_variations import variations as hi_variations
from indic_numtowords.mal.data.user_variations import variations as ml_variations
from indic_numtowords.mar.data.user_variations import variations as mr_variations
from indic_numtowords.ori.data.user_variations import variations as or_variations
from indic_numtowords.pun.data.user_variations import variations as pa_variations
from indic_numtowords.tam.data.user_variations import variations as ta_variations
from indic_numtowords.tel.data.user_variations import variations as te_variations
from indic_numtowords.kan.data.user_variations import variations as kn_variations
from indic_numtowords.urd.data.user_variations import variations as ur_variations

from indic_numtowords.doi.data.nums import DIRECT_DICT as doi_direct_dict
from indic_numtowords.sat.data.nums import DIRECT_DICT as sat_direct_dict
from indic_numtowords.mai.data.nums import DIRECT_DICT as mai_direct_dict
from indic_numtowords.sd.data.nums import DIRECT_DICT as sd_direct_dict
from indic_numtowords.brx.data.nums import DIRECT_DICT as brx_direct_dict

from indic_numtowords.doi.data.nums import EXCEPTIONS_DICT as doi_exceptions_dict
from indic_numtowords.sat.data.nums import EXCEPTIONS_DICT as sat_exceptions_dict
from indic_numtowords.mai.data.nums import EXCEPTIONS_DICT as mai_exceptions_dict
from indic_numtowords.sd.data.nums import EXCEPTIONS_DICT as sd_exceptions_dict
from indic_numtowords.brx.data.nums import EXCEPTIONS_DICT as brx_exceptions_dict

from indic_numtowords.doi.utils import split_number as doi_split_number
from indic_numtowords.sat.utils import split_number as sat_split_number
from indic_numtowords.mai.utils import split_number as mai_split_number
from indic_numtowords.sd.utils import split_number as sd_split_number
from indic_numtowords.brx.utils import split_number as brx_split_number

from indic_numtowords.doi.cardinal import process_text as doi_process_text
from indic_numtowords.sat.cardinal import process_text as sat_process_text
from indic_numtowords.mai.cardinal import process_text as mai_process_text
from indic_numtowords.sd.cardinal import process_text as sd_process_text
from indic_numtowords.brx.cardinal import process_text as brx_process_text

supported_langs = ('as', 'bn', 'en', 'gu', 'hi', 'ml', 'mr', 'or', 'pa', 'ta', 'te', 'kn', 'ur')
extended_supported_langs = ('doi', 'sat', 'mai', 'sd', 'brx')

lang_func_dict = {
    'as': as_convert,
    'bn': bn_convert,
    'en': en_convert,
    'gu': gu_convert,
    'hi': hi_convert,
    'ml': ml_convert,
    'mr': mr_convert,
    'or': or_convert,
    'pa': pa_convert,
    'ta': ta_convert,
    'te': te_convert,
    'kn': kn_convert,
    'ur': ur_convert
}

user_variation_file_map = {
    'as' : as_variations,
    'bn' : bn_variations,
    'en' : en_variations,
    'gu' : gu_variations,
    'hi' : hi_variations,
    'ml' : ml_variations,
    'mr' : mr_variations,
    'or' : or_variations,
    'pa' : pa_variations,
    'ta' : ta_variations,
    'te' : te_variations,
    'kn' : kn_variations,
    'ur' : ur_variations
}

direct_dict_mapping = {
    'doi': doi_direct_dict,
    'sat': sat_direct_dict,
    'mai': mai_direct_dict,
    'sd': sd_direct_dict,
    'brx': brx_direct_dict
}

exceptions_dict_mapping = {
    'doi': doi_exceptions_dict,
    'sat': sat_exceptions_dict,
    'mai': mai_exceptions_dict,
    'sd': sd_exceptions_dict,
    'brx': brx_exceptions_dict
}

split_number_mapping = {
    'doi': doi_split_number,
    'sat': sat_split_number,
    'mai': mai_split_number,
    'sd': sd_split_number,
    'brx': brx_split_number
}

process_text_mapping = {
    'doi': doi_process_text,
    'sat': sat_process_text,
    'mai': mai_process_text,
    'sd': sd_process_text,
    'brx': brx_process_text
}

def num2words(num, lang = 'en', variations = False, split=False, script=False):
    if lang in extended_supported_langs:
        return num2words_extended(num, lang=lang, variations=variations, split=split, script=script)

    if lang not in supported_langs:
        raise ValueError(f"Language not supported. Please check the language code.")
    
    results = lang_func_dict[lang](num)
    if variations == False:
        return results[0]
    variations = list(set(get_variations(num, lang)))
    results.extend(variations)
    results = [re.sub(r"[\u200c\u200b]", "", line) for line in results]
    return results

def num2words_extended(number: int | str, lang: str, variations: bool = False, split: bool = False, script: bool = False) -> str | list:
    """
    Convert a number to its textual representation in a specified Indian language.

    Args:
        number (int or str): The number to convert, provided as an integer or a numeric string.
        lang (str): The language code representing the target Indian language for conversion.
        variations (bool, optional): Returns a list of possible textual variations if set to True. Defaults to False.
        split (bool, optional): Converts each digit separately into its word form when set to True. Defaults to False.
        script (bool, optional): Processes the number in a specific script format if set to True. Defaults to False.

    Returns:
        str: The textual representation of the number if `variations` is False.
        list[str]: A list of textual variations if `variations` is True.

    Raises:
        ValueError: If the input is not a valid number.
    """
    if isinstance(number, str):
        number = number.strip().replace(',', '')
        if not number.isdigit():
            raise ValueError("Input string must be a valid number")

    number_str = str(number).lstrip('0') or '0'

    if lang in ('sat', 'brx'):
        extended = len(number_str) > 9
    else:
        extended = len(number_str) > (19 if script else 9)
    
    if extended or split:
        return " ".join(direct_dict_mapping[lang][digit][0] for digit in (number if split else number_str))

    numbers = split_number_mapping[lang](number_str)
    converted_text = []

    for index, num in enumerate(numbers):
      converted_text = process_text_mapping[lang](num, converted_text, index, len(number_str))

    exceptions = exceptions_dict_mapping[lang].get(number_str, [])
    final_text = [re.sub(r'[\u200c\u200b]', '', i) for i in converted_text] + exceptions

    return final_text if variations else final_text[0]


def add_variation(num, word, lang):
    user_variation_file = user_variation_file_map[lang]
    user_variation_dict = dict()

    with open(user_variation_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            user_variation_dict[row[0]] = list(row[1:])

    if num in user_variation_dict:
        user_variation_dict[num].append(word)
    else:
        user_variation_dict[num] = [word]
    
    with open(user_variation_file, 'w') as f:
        for num in user_variation_dict.keys():
            line = num + '\t'
            for word in user_variation_dict[num]:
                line += word + '\t'
            line = line.strip()
            line += '\n'
            f.write(line)


def get_variations(num, lang):
    user_variation_dict = user_variation_file_map[lang]

    if int(num) in user_variation_dict:
        return set(user_variation_dict[int(num)])
    else:
        return set()
