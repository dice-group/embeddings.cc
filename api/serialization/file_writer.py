# This Python class writes embeddings.cc data files.
# The data files can be in bzip2 or text format.
#
# Example usage:
# from file_writer import FileWriter
# data = {}
# data['http://example.com/0'] = [0,1,2,3,4,5,6,7,8,9]
# data['http://example.com/1'] = [1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,0.0]
# writer = FileWriter(id='test', format='bzip2')
# writer.open()
# for item in data.items():
#     writer.add(item[0], item[1])
# writer.close()

import bz2

class FileWriter:
    FORMAT_BZIP2 = 'bzip2'
    FORMAT_TEXT = 'txt'

    def __init__(self, id, format=None):
        self.id = id
        if format is None:
            self.format = FileReader.FORMAT_BZIP2
        else:
            self.format = format

    def open(self):
        if self.format is self.FORMAT_BZIP2:
            self.f_embs = bz2.open(self.id + '.embeddings.txt.bz2', mode='wt', compresslevel=9, encoding=None, errors=None, newline=None)
            self.f_uris = bz2.open(self.id + '.uris.txt.bz2', mode='wt', compresslevel=9, encoding=None, errors=None, newline=None)
        elif self.format is self.FORMAT_TEXT:
            self.f_embs = open(self.id + '.embeddings.txt', 'w')
            self.f_uris = open(self.id + '.uris.txt', 'w')
        else:
            raise NameError('Unknown format: ' + self.format)

    def add(self, uri, embeddings):
        if not uri.startswith('http://') and not uri.startswith('https://'):
            print('Skipping URI with unknown protocol:', uri)
            return
        if not type(embeddings) is list:
            raise TypeError('Embeddings not provided as list of floats:', uri, embeddings)
        for number in embeddings:
            if not type(number) is float and  not type(number) is int:
                raise TypeError('Embeddings not provided as list of floats:', uri, embeddings)
        self.f_embs.write(",".join(str(emb) for emb in embeddings) + '\n')
        self.f_uris.write(uri + '\n')

    def close(self):
        self.f_uris.close()
        self.f_embs.close()
