
# coding: utf-8

# In[ ]:


"""
Author: Aron
Name : MWT(Mongolian Word Tokenizer)
"""


# In[65]:


import os, sys, string
from os import path
from progressbar import ProgressBar
from icu import UnicodeString, BreakIterator, Locale
from collections import defaultdict

import time
import argparse
import click


# In[62]:


from nltk import word_tokenize
# nltk.download('punkt')


# In[3]:


def containsMongolianChar(word):
    for ch in word:
        if 0x1800 < ord(ch) < 0x18ff:
            return True
    return False


# In[69]:


MONGOLIAN_PUNCTUATIONS = "".join([chr(w) for w in range(0x1800,0x180a)])
MONGOLIAN_DIGISTS = "".join([chr(w) for w in range(0x1810,0x181a)])
MONGOLIAN_CONTROL_CHAR = "".join([chr(w) for w in range(0x180b,0x180f)])+"\u200d"
# CodeStr(MONGOLIAN_CONTROL_CHAR)


# In[4]:


STRIP_CHARS = string.ascii_letters             + string.whitespace             + string.punctuation             + string.digits             + MONGOLIAN_PUNCTUATIONS             + MONGOLIAN_DIGISTS             + "\u3008\u00b7\u00a7\u00ab<>\u300a\u3000\u300b\u1804\u1802\u1803\u0028\u0029\ufe15\ufe16\u7267\u6B4C\u2014\u00a0\u00ad\u00BA\u0020\u1802\u1803"


# In[59]:


def splitStemAndSuffix(word):
    """
    split word to stem and suffixes
    """
    ls = word.split("\u202f")
    if len(ls) > 1:
        return ls[0], ["\u202f" + s for s in ls[1:]]
    else:
        return None, None
# stem, suffix = splitStemAndSuffix("asdf")


# In[ ]:


def CodeStr(text):
    ls = []
    for ch in text:
        ls.append(ord(ch))
    return ",".join(["%04X"%(c) for c in ls])


# In[11]:


def split_line_with_icu(line):
    boundary = BreakIterator.createWordInstance(Locale.getUS())
    # text = "dasdf asdf asd f"
    boundary.setText(line)
    
    word_list = []
    
    start = boundary.first()
#         ls =[]
    for end in boundary:
        word = line[start:end ]
        word = word.strip(STRIP_CHARS)
        if ( word.strip() != "") and ( word.strip(MONGOLIAN_CONTROL_CHAR) != "" ) and (word.strip(MONGOLIAN_CONTROL_CHAR) != "") and containsMongolianChar(word) :
            word_list.append(word)
        start = end
    return word_list


# In[10]:


def split_line_with_py(line):
    
    word_list_ = line.split(" ")
    word_list = []
    for word in word_list_:
        word = word.strip(STRIP_CHARS)
        if not word.strip() == "" and containsMongolianChar(word):
            word_list.append(word)
    return word_list
        


# In[7]:


@click.command()
@click.option('--input-file', "-f", type=click.Path(exists=True), help='Input file' ,required=True)
@click.option('--output-file', "-o", type=click.Path(exists=True), help='Output file', required=True)
@click.option('--strip-mongolian-suffix', "-s", type=click.Choice(['yes', 'no']), help='strip-mongolian-suffix', default="no")
# @click.option('--splitter', "-s", type=click.Path(), help='Output file', required=True)
# @click.option('--with-icu-break', "-i", type=click.Path(), help='Output file', required=True)
# @click.option('--with-python', "-p", type=click.Path(), help='Output file', required=True)
# @click.option('--with-icu', "-n", type=click.Path(), help='Output file', required=True)
def main(input_file, output_file, strip_mongolian_suffix):
#     click.echo(input_file)
#     click.echo(output_file)
    
        
    
    word_dict = defaultdict(lambda :0)
    p = ProgressBar()
#     r = opendb()
    outfile_path =""
    
    
    split_line = split_line_with_icu
        
    
    
    with open(input_file, "r") as in_file:
        for i, line in enumerate(p(in_file)):
            p.update(i + 1)
            line = line.strip()
            if line == "":
                continue
            for word in split_line(line):
                ## word_dict[word] += 1
                stem, suffix = splitStemAndSuffix(word)
                if stem is None:
                    word_dict[word] += 1
                else:
                    if (not stem.strip() == "") and containsMongolianChar(stem):
                        word_dict[stem] += 1
                    if strip_mongolian_suffix == "no":
                        for suf in suffix:
                            word_dict[suf] += 1
    #                 ss = r.get(word)
    #                 if ss is None:
    #                     r.set(word, str(i))
    #                 else:
    #                     text = ss.decode("utf-8")
    #         #                 print(text)
    #                     ls = text.split(",")
    #                     ls.append(str(i))
    #                     r.set(word, ",".join(set(ls)))         
    with open(output_file, "w") as out_file:
        for word, count in sorted(word_dict.items(), key =lambda a: a[0]):
            print(word, CodeStr(word), count, file = out_file)
            


# In[ ]:


if __name__ == '__main__':
    
    
    main()
    
    

