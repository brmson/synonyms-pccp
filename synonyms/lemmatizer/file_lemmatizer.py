#!/usr/bin/python3
import os, re, csv, argparse, subprocess
dir_cur = os.path.dirname(os.path.realpath(__file__))
TOKENIZER_CMD = os.path.join(dir_cur, "tokenizer/run_tokenizer_f")
MORPHOLOGY_CMD = os.path.join(dir_cur, "morphology/run_morphology_f")



LEMMA_ADDINFO_RE = re.compile(
    "((?<=.)-\d+|`.|_:[NJAZMVTWDPCIFBQX]|_;[YSEGKRmHULjgcybuwpzo]|_,[tnashelvx]|_\^\(.*\)).*$")



def lemmatize(words):
    iname = '/tmp/input%d' % len(words)
    oname = '/tmp/output%d' % len(words)
    with open(iname, 'w', encoding='iso-8859-2') as ifile:
        ifile.write(' '.join(words)+'\n')
    file_lemmatizer(iname, oname)
    lemmatized_words = []
    with open(oname) as ofile:
        for line in ofile:
            word, lemma, tags = line.split()
            lemmatized_words.append(lemma)
    os.remove(iname)
    os.remove(oname)
    return lemmatized_words


def file_lemmatizer(input_file, output_file):
    try:
        subprocess.check_call([" ".join([TOKENIZER_CMD, input_file, input_file + ".tokenized"])], shell=True)
        subprocess.check_call([" ".join([MORPHOLOGY_CMD, input_file + ".tokenized", input_file + ".tagged"])],
                              shell=True)
        os.remove(input_file + ".tokenized")
        with open(input_file + ".tagged", 'r', encoding='iso8859-2') as ifile:
            with open(output_file, 'w', encoding='utf-8') as ofile:
                writer = csv.writer(ofile, delimiter='\t', quotechar='', quoting=csv.QUOTE_NONE, lineterminator='\n')
                for row in csv.reader(ifile, delimiter='\t', quoting=csv.QUOTE_NONE):
                    writer.writerow([row[0].strip(), LEMMA_ADDINFO_RE.sub('', row[1].strip()), row[2].strip()])
        os.remove(input_file + ".tagged")
    except subprocess.CalledProcessError as err:
        print(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="TODO: Write this help description...")
    parser.add_argument("input_file", help="Specified file to lemmatize.")
    parser.add_argument("output_file", help="Specifies output file.")

    arguments = parser.parse_args()

    if not (os.path.exists(arguments.input_file)):
        raise SystemExit("ERROR: <input_file> has to be a file!")

    file_lemmatizer(os.path.abspath(arguments.input_file), os.path.abspath(arguments.output_file))
    
        


