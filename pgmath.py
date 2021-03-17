import pygame as pg
from math import *

scale = lambda tx, scale: pg.transform.scale(tx, tuple([tx.get_size()[i] * scale for i in range(2)]))

abs_length = lambda rel_length, full_length: rel_length * full_length / 100
rel_length = lambda abs_length, full_length: abs_length / full_length * 100
abs_size = lambda rel_size, full_size: tupdiv(tupmult(rel_size, full_size), 100)
rel_size = lambda abs_size, full_size: tupmult(tupdiv(abs_size, full_size), 100)

def merge(*args): #Merge dictionaries together, and add elements with the same key in a list together with that key
    returndict = {}
    for d in args:
        for k, v in d.items():
            if k not in returndict.keys():
                returndict[k] = v
                continue
            if type(returndict[k]) == tuple: returndict[k] = list(returndict[k])
            elif type(returndict[k]) != list: returndict[k] = [returndict[k]]
            if type(v) not in (list, tuple):
                returndict[k].append(v)
                continue
            for i in v: returndict[k].append(i)
    return returndict

def _arg_setup(*args):
    tuplength = len(args[0])
    args = [tup if type(tup) in (tuple, list) else (tup,) * tuplength for tup in args]
    return args

def _tup_func(func, *tups):
    tups = list(tups)
    first_tup = tups.pop(0)
    for tup in tups:
        first_tup = map(func, first_tup, tup)
    return first_tup

def _tupmath(op, *tups):
    tups = [arg.center if type(arg) == pg.Rect else arg for arg in tups]
    tups = _arg_setup(*tups)
    result = _tup_func(op, *[[float(num) for num in tup] for tup in tups])
    return [int(num) if num.is_integer() else num for num in result]

tupadd = lambda *tups: _tupmath(float.__add__, *tups)
tupsub = lambda *tups: _tupmath(float.__sub__, *tups)
tupmult = lambda *tups: _tupmath(float.__mul__, *tups)
tupdiv = lambda *tups: _tupmath(float.__truediv__, *tups)

def tupmethod(tup, method, *args, **kwargs): #Call a method on every element in a tuple
    tup = tuple(method(elem, *args, **kwargs) for elem in tup)
    return tup

def advancedmap(funcs, *tups):
    tups = _arg_setup(*tups)
    tups = zip(*tups)
    return tuple(func(*tup) for func, tup in zip(funcs, tups))

def get_distance(rect1, rect2): #Get distance between 2 rects using the pythagorean theorem
    delta = tupsub(rect2.center, rect1.center)
    return sqrt(delta[0]**2 + delta[1]**2)
