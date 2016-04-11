import sys, os
from ufal.morphodita import TaggedLemmas, Tagger, Forms, TokenRanges
from ufal.nametag import NamedEntities, Ner
from synonyms.in_out.readers import open_gz

dir_cur = os.path.dirname(os.path.realpath(__file__))


def sort_entities(entities):
    return sorted(entities, key=lambda entity: (entity.start, -entity.length))


def lemmatize(file, output_file):
    morphodita_model = '/home/vesely/Research/Synonyms/synonyms/lemmatizer/czech-morfflex-pdt-131112-raw_lemmas.tagger-best_accuracy'
    tagger = Tagger.load(morphodita_model)
    assert tagger
    forms = Forms()
    lemmas = TaggedLemmas()
    tokens = TokenRanges()
    tokenizer = tagger.newTokenizer()
    assert tokenizer
    with open_gz(output_file, 'w') as out, open_gz(file) as f:
        for line in f:
            tokenizer.setText(line)
            while tokenizer.nextSentence(forms, tokens):
                tagger.tag(forms, lemmas)
                # for i in range(len(tokens)):
                # lemma = lemmas[i]
                # token = tokens[i]
                #word = line[token.start:token.start + token.length]
                #out.write(str(lemma.lemma) + ' ')
                #out.write(" ".join(list(map(lambda x: str(x.lemma), lemmas))))
                out.write(" ".join(list(map(lambda x: str(x.lemma).strip() + '___' + str(x.tag).strip(), lemmas))))
            out.write('\n')


class Morphodita:
    def __init__(self):
        self.morphodita_model = os.path.join(dir_cur, 'czech-morfflex-131112.tagger-fast')
        self.tagger = Tagger.load(self.morphodita_model)
        self.forms = Forms()
        self.lemmas = TaggedLemmas()
        self.tokens = TokenRanges()
        self.tokenizer = self.tagger.newTokenizer()

    def lemmatize(self, text):
        self.tokenizer.setText(text)
        lemmas = []
        while self.tokenizer.nextSentence(self.forms, self.tokens):
            self.tagger.tag(self.forms, self.lemmas)
            lemmas += [str(x.lemma).strip() for x in self.lemmas]
        return lemmas


def lemmatize_and_replace_entities(file, output_file):
    nametag_model = os.path.join(dir_cur, 'czech-cnec2.0-140304.ner')
    morphodita_model = os.path.join(dir_cur, 'czech-morfflex-131112.tagger-fast')
    tagger = Tagger.load(morphodita_model)
    assert tagger
    ner = Ner.load(nametag_model)
    assert ner
    forms = Forms()
    lemmas = TaggedLemmas()
    tokens = TokenRanges()
    entities = NamedEntities()
    tokenizer = ner.newTokenizer()
    assert tokenizer
    with open_gz(output_file, 'w') as out, open_gz(file) as f:
        for line in f:
            tokenizer.setText(line)
            while tokenizer.nextSentence(forms, tokens):
                tagger.tag(forms, lemmas)
                ner.recognize(forms, entities)
                sorted_entities = sort_entities(entities)
                open_entities = []
                open_entities_type = []
                e = 0
                for i in range(len(tokens)):
                    lemma = lemmas[i]
                    token = tokens[i]
                    word = line[token.start:token.start + token.length]
                    while e < len(sorted_entities) and sorted_entities[e].start == i:
                        open_entities.append(sorted_entities[e].start + sorted_entities[e].length - 1)
                        open_entities_type.append(sorted_entities[e].type)
                        e += 1
                    if len(open_entities) == 0:
                        out.write(str(lemma.lemma) + ' ')
                    else:
                        out.write("@!ENT!%s " % ('!'.join(open_entities_type)))
                    while open_entities and open_entities[-1] == i:
                        open_entities.pop()
                        open_entities_type.pop()
            out.write('\n')