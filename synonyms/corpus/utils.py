__author__ = 'veselt12'
import xml.etree.ElementTree as ET
import gzip
from synonyms.in_out.readers import open_gz


def syn2_to_plain(filename, filename_out, keep_punctuation=True, keep_tags=False, raw=False):
    with open_gz(filename_out, 'w') as file, open_gz(filename, 'r', encoding='utf-8') as f:
        root = ET.iterparse(f)
        for event, element in root:
            if element.tag == 'block':
                file.write('\n')
            if element.tag == 's':
                file.write(' '.join(element.text.split()[::3]))
                # for word in element.text.split('\n'):
                #     if word:
                #         word, lemma, tags = word.split('\t')
                #         if raw:
                #             file.write(word + ' ')
                #         elif keep_tags:
                #             file.write(word + ' ' + lemma + ' ' + tags + '\n')
                #         elif keep_punctuation or not tags.startswith('Z'):
                #             file.write(lemma + ' ')
                file.write('\n')
            element.clear()


def syn2_to_plain2(filename, filename_out, keep_punctuation=True):
    with open(filename_out, 'w', encoding='utf-8') as file:
        with open(filename) as ff:
            for line in ff:
                word, lemma, tags = line.split('\t')
                if keep_punctuation or not tags.startswith('Z'):
                    file.write(lemma + ' ')
                if tags.startswith('Z') and word in ['.', '?', '!']:
                    file.write('\n')