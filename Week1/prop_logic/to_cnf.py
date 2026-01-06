import json
import os
import sys
from typing import List, Set, Dict, Tuple, Any

class Expr:
    pass


class Var(Expr):
    def __init__(self, name):
        self.name = name


class Not(Expr):
    def __init__(self, expr):
        self.expr = expr


class And(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Or(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

def rem_implies(expr):
    if isinstance(expr,Var):
        return expr
    elif isinstance(expr,Implies):
        return Or(Not(rem_implies(expr.left)),rem_implies(expr.right))
    elif isinstance(expr,Not):
        return Not(rem_implies(expr.expr))
    elif isinstance(expr,And):
        return And(rem_implies(expr.left),rem_implies(expr.right))
    elif isinstance(expr,Or):
        return Or(rem_implies(expr.left),rem_implies(expr.right))
    
    return expr
    
def negationPush(expr):
    if isinstance(expr,Var):
        return expr
    
    elif isinstance(expr,Not):
        ins = expr.expr
        if isinstance(ins,Var):
            return expr
        elif isinstance(ins,Not):
            return negationPush(ins.expr)
        elif isinstance(ins,And):
            return Or(negationPush(Not(ins.left)),negationPush(Not(ins.right)))
        elif isinstance(ins,Or):
            return And(negationPush(Not(ins.left)), negationPush(Not(ins.right)))
    
    elif isinstance(expr,And):
        return And(negationPush((expr.left)),negationPush((expr.right)))
    elif isinstance(expr,Or):
        return Or(negationPush((expr.left)), negationPush((expr.right)))
    
    return expr
    
def orDistribution(expr):
    if isinstance(expr,Var) or isinstance(expr,Not):
        return expr
    if isinstance(expr.left,Var) and isinstance(expr.right,Var):
        return expr
    if isinstance(expr,And):
        return And(orDistribution(expr.left),orDistribution(expr.right))
    else:
        left = orDistribution(expr.left)
        right = orDistribution(expr.right)
        if isinstance(left,And):
            return And(orDistribution(Or(left.left,right)), 
                       orDistribution(Or(left.right,right)))
        elif isinstance(right,And):
            return And(orDistribution(Or(right.left,left)),
                       orDistribution(Or(right.right,left)))
        return Or(left,right)
    
    return expr

def clauses(expr) -> List[Set[str]]:
    if isinstance(expr,And):
        return clauses(expr.left) + clauses(expr.right)
    else:
        return [get_literals(expr)]
        

def get_literals(e) -> Set[str]:
    if isinstance(e,Var):
        return {e.name}
    if isinstance(e,Not):
        return {"~" + e.expr.name}
    if isinstance(e,Or):
        return get_literals(e.left) | get_literals(e.right)


def to_cnf(expr):
    """
    Converts a propositional logic expression to CNF.
    Returns a list of clauses, each clause is a set of literals.
    """
    expr1 = rem_implies(expr)
    e2 = negationPush(expr1)
    e3 = orDistribution(e2)
    return clauses(e3)
    raise NotImplementedError
