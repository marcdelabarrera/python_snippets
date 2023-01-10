# This file needs to start by test_ to be recognized by pytest
import sys
import os
sys.path.append(os.path.abspath('.'))

from module import foo

def test_foo():
    assert foo(2)==3

def test_something():
    assert 1+1== 2