#!/usr/bin/python3


import os, re, csv, argparse, subprocess, queue, multiprocessing, traceback, sys, time
from threading import Thread


class TokenizerWorker(Thread):

    TOKENIZER_CMD = "./tokenizer/run_tokenizer_f"
    MORPHOLOGY_CMD = "./morphology/run_morphology_f"
    
    LEMMA_ADDINFO_RE = re.compile("((?<=.)-\d+|`.|_:[NJAZMVTWDPCIFBQX]|_;[YSEGKRmHULjgcybuwpzo]|_,[tnashelvx]|_\^\(.*\)).*$")

    def __init__(self, queue, inputdir, outputdir):
        Thread.__init__(self)
        self._queue = queue
        self._outputdir = outputdir
        self._inputdir = inputdir

    def _process(self, filename):
        try:
            subprocess.check_call([" ".join([self.TOKENIZER_CMD, os.path.join(self._inputdir, filename), os.path.join(self._inputdir, filename + ".tokenized")])], shell = True)
            subprocess.check_call([" ".join([self.MORPHOLOGY_CMD, os.path.join(self._inputdir, filename + ".tokenized"), os.path.join(self._inputdir, filename + ".tagged")])], shell = True)

            os.remove(os.path.join(self._inputdir, filename + ".tokenized"))

            with open(os.path.join(self._inputdir, filename + ".tagged"), 'r', encoding='iso8859-2') as ifile:
                with open(os.path.join(self._outputdir, filename), 'w', encoding='utf-8') as ofile:
                    writer = csv.writer(ofile, delimiter='\t', quotechar='', quoting=csv.QUOTE_NONE, lineterminator='\n')
                    for row in csv.reader(ifile, delimiter='\t', quoting=csv.QUOTE_NONE):
                        writer.writerow([row[0].strip(), self.LEMMA_ADDINFO_RE.sub('', row[1].strip()), row[2].strip()])

            os.remove(os.path.join(self._inputdir, filename + ".tagged"))
        except subprocess.CalledProcessError as err:
            print(err)

    def run(self):
        while True:
            filepath = None
            try:
                filepath = self._queue.get(timeout = 1)
                if filepath is not None:
                    self._process(filepath)
            except queue.Empty:
                break
            except:
                traceback.print_exc(file = sys.stdout)
            finally:
                if filepath is not None:
                     self._queue.task_done()


def main(inputdir, outputdir, verbose):
    # Initializes a queue for files
    file_queue = queue.Queue()
    for filename in os.listdir(inputdir):
        file_queue.put(filename)

    nfiles = file_queue.qsize()

    if verbose:
        sys.stdout.write("\rProcessed: 0 of {0} files ( 0%)".format(nfiles, nfiles))

    # Starts the workers.
    workers = []
    for _ in range(multiprocessing.cpu_count()):
        worker = TokenizerWorker(file_queue, inputdir, outputdir)
        worker.setDaemon(True)
        worker.start()
        workers.append(worker)

    # Wait until the queue empties out.
    if verbose:
        while not file_queue.empty():
            nprocessed = nfiles - file_queue.unfinished_tasks
            sys.stdout.write("\rProcessed: {0} of {1} files ({2:2d}%)".format(nprocessed, nfiles, 100 * nprocessed // nfiles))
            sys.stdout.flush()
            time.sleep(0.5)
    else:
        file_queue.join()

    # Wait until all the workers have finished their job.
    for worker in workers:
        worker.join()

    if verbose:
        sys.stdout.write("\rProcessed: {0} of {1} files (Done!)\n".format(nfiles, nfiles))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, description = "TODO: Write this help description...")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "If present progress specific messages will be printed out.")
    parser.add_argument("inputdir", help = "Specifies directory with documents to lemmatize.")
    parser.add_argument("outputdir", help = "Specifies output directory for lemmatized documents.")

    arguments = parser.parse_args()

    if not (os.path.exists(arguments.inputdir) and os.path.isdir(arguments.inputdir)):
        raise SystemExit("ERROR: <inputdir> has to be a directory!")

    try:
        if os.path.abspath(arguments.inputdir) == os.path.abspath(arguments.outputdir):
            raise SystemExit('ERROR: Output directory has to be different from input directory!')

        if not os.path.exists(arguments.outputdir):
            try:
                os.makedirs(arguments.outputdir, exist_ok = True)
            except OSError:
                raise SystemExit("ERROR: Couldn't create or access the output directory: '{0}'".format(arguments.outputdir))

        if not os.path.isdir(arguments.outputdir):
            raise SystemExit("ERROR: <outputdir> has to be a directory!")
    except OSError:
        raise SystemExit("ERROR: Couldn't create or access the output directory: {0}".format(arguments.outputdir))

    try:
        main(os.path.abspath(arguments.inputdir), os.path.abspath(arguments.outputdir), arguments.verbose)
    except:
        if arguments.verbose:
            sys.stdout.write('\n')
        raise



