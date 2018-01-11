###############################################################################
# Author: Danny Ly (RedKlouds)
# File Name: test_display_text.py
# Program Description:
# Percondition:
# Postcondition:
#------------------------------------------------------------------------------
# Creation Date: January 09, 2018
# Last Modified: Tue 09 Jan 2018 11:41:00 AM UTC
###############################################################################
import unittest

from engines import display_text

def test_sample_single_word():
    l = ('foo', 'bar', 'foobar')
    word = display_text.sample(l)
    assert word in l

def test_sample_multiple_words():
    l = ('foo', 'bar', 'foobar')
    words = display_text.sample(l, 2)
    assert len(words) == 2
    assert words[0] in l
    assert words[1] in l
    assert words[0] is not words[1]

def test_generate_buzz_of_at_least_five_words():
    phrase = display_text.generate_buzz()
    assert len(phrase.split()) >= 5

