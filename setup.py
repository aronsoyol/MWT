
# coding: utf-8

# In[1]:


#!/usr/bin/env python

from distutils.core import setup

setup(name='tmt',
      version='1.0',
      description='Traditional Mongolian Tokenizer',
      author='Aronsoyol',
      author_email='aronsoyol@gmail.com',
      url='https://github.com/aronsoyol/tmt',
      install_requires=["click"],
      packages=['tmt'],
     )

