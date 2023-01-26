# This Python class reads embeddings.cc data files.
# The data files can be in bzip2 or text format.
#
# Example usage:
# from file_reader import FileReader
# data = []
# for item in FileReader(embeddings_file='example.embeddings.txt.bz2', uri_file='example.uris.txt.bz2', format='bzip2'):
#     data.append((item[0], item[1]))
# print('Types:          ', type(data[0]), type(data[0][0]), type(data[0][1]), type(data[0][1][0]))
# print('Dimensions:     ', len(data[-1][1]))
# print('First item:     ', data[0])
# print('Last item:      ', data[-1])
# print('Number of items:', len(data))

import bz2

class FileReader:
    FORMAT_BZIP2 = 'bzip2'
    FORMAT_TEXT = 'txt'

    def __init__(self, embeddings_file=None, uri_file=None, format=None):
        self.embeddings_file = embeddings_file
        self.uri_file = uri_file
        if format is None:
            self.format = FileReader.FORMAT_BZIP2
        else:
            self.format = format

    def __iter__(self):
        if self.format is self.FORMAT_BZIP2:
            f_embs = bz2.open(self.embeddings_file, mode='rt',encoding="utf-8")
            f_uris = bz2.open(self.uri_file, mode='rt',encoding="utf-8")
        elif self.format is self.FORMAT_TEXT:
            f_embs = open(self.embeddings_file, 'r')
            f_uris = open(self.uri_file, 'r')
        else:
            raise NameError('Unknown format: ' + self.format)

        while True:
            uri = f_uris.readline().rstrip()
            emb = f_embs.readline().rstrip()
            if not uri or not emb:
                break
            else:
                yield (uri, [float(numeric_string) for numeric_string in emb.split(',')])

        f_uris.close()
        f_embs.close()
