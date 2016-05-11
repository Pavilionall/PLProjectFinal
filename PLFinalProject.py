#------------------------------------------------------------
# HMM tokenizer
# ------------------------------------------------------------

import ply.lex as lex

# Dictionary to store variable names and values
global variableDict
variableDict = {}

#list to store names in function library
funcList= []
funcList.append("squares")
funcList.append("squareSum")
funcList.append("varAdd")

# Reserved words
reserved = {
    'IF'     : 'if',
    'IFF'    : 'iff',
    'ELSE'   : 'else',
    'WHILE'  : 'while',
    'FOR'    : 'for',
    'INT'    : 'int',
    'FLOAT'  : 'float',
    'BOOL'   : 'bool',
    'VOID'   : 'void',
    'LIST'   : 'list',
    'TUPLE'  : 'tuple',
    'OBJECT' : 'object',
    'STRING' : 'string',
    'RETURN' : 'return',
    'TRUE'   : 'TRUE',
    'FALSE'  : 'FALSE',

}

# List of token names.
tokens = [
          'AND_OP', 'OR_OP', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LCURLY', 'RCURLY', \
          'SEMI', 'EQ_OP', 'NE_OP', 'LE_OP', 'GE_OP', 'ELEM', 'PIPE', 'EQUALS', \
          'LT_OP', 'GT_OP', 'PLUS', 'MINUS', 'MULT', 'DIV', 'PRCNT', 'BANG', \
          'COMMA', 'SQUOTE', 'LAMBDA', 'MAP_TO', \
          #'DOT', \
          'INTEGER', 'IDENTIFIER', 'CLFLOAT', 'CLSTRING','FUNCTION_CALL' \
          ] + list(reserved.keys())

# Regular expression rules for simple tokens

def t_CLFLOAT(t):
    r'[0-9]+[\.][0-9]*'
    return t

t_AND_OP = r'&&'
t_OR_OP  = r'\|\|'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\['
t_RBRACE = r']'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_SEMI   = r';'
t_EQ_OP  = r'=='
t_NE_OP  = r'!='
t_LE_OP  = r'<='
t_GE_OP  = r'>='
t_ELEM   = r'<-'
t_PIPE   = r'\|'
t_EQUALS = r'='
t_LT_OP  = r'<'
t_GT_OP  = r'>'
t_MINUS  = r'-'
t_PLUS   = r'\+'
t_MULT   = r'\*'
t_DIV    = r'/'
t_PRCNT  = r'%'
t_BANG   = r'!'
t_COMMA  = r','
t_SQUOTE = r"'"
#t_DOT    = r'.'
t_LAMBDA = r'\(\\'
t_MAP_TO = r'->'


# Boolean method returns True if float
def isFloat(num):
    num = str(num)
    if ("." not in num):
        return False
    else:
        return True

# Extract variable values from a list of numbers and variables
def extractVals(list):
    numList = []
    for i in list:
        if i in variableDict:
            numList.append(variableDict[i])
        elif isFloat(i):
            numList.append(float(i))
        else:
            numList.append(int(i))
    return numList

#Evaluate the right hand side of an expresion if it has more than one term.
def evalStr(string):
    x = string[0]
    y = string[2]

    if isFloat(x):
        x = float(x)
    else:
        x = int(x)

    if isFloat(y):
        y = float(y)
    else:
        y = int(y)

    if (string[1] == "+"):
        from java.lang import Math
        import Arithmetic
        return Arithmetic.add(x, y)
    if (string[1] == "*"):
        from java.lang import Math
        import Arithmetic
        return Arithmetic.mult(x, y)
    if (string[1] == "-"):
        from java.lang import Math
        import Arithmetic
        return Arithmetic.subract(x, y)
    if (string[1] == "/"):
        from java.lang import Math
        import Arithmetic
        return Arithmetic.div(x, y)

#Using Java Streams prints out the square of each of the elements in a list
def squares(items):
    temp = ""
    for i in items:
        temp += str(i)
        temp += ","
    print "The squares of ", items, " are:"
    import Arithmetic
    Arithmetic.squares(temp)

def squareSum(items):
    sum = 0
    squareList = [i*i for i in items]
    for i in squareList:
        sum += i
    print sum, "sqaures"

def plusN(item, n):
    return item + n


def varAdd(n):
    global variableDict
    print "Current variable dictionary: ", variableDict
    variableDictUpdate = {k: plusN(v, n[0]) for k, v in variableDict.iteritems()}
    variableDict.clear()
    variableDict = variableDictUpdate
    print "Variable dictionary after varAdd(" + str(n[0]) + "): ", variableDict

def t_INTEGER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Line %d: Number %s is too large!" % (t.lineno,t.value)
        t.value = 0
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in reserved:
        print "In t_IDENTIFIER, saw: ", t.value
        t.type = t.value.upper()

    return t

def t_FUNCTION_CALL(t):
    r'\*[a-zA-Z0-9_]*\([. ,a-zA-Z0-9_]*\);'
    if t.value.upper() in reserved:
        print "In t_IDENTIFIER, saw: ", t.value
        t.type = t.value.upper()
    print t.value
    i = 0
    counter = 0
    initLength = 0
    #get the length of the function name
    while t.value[i] != '(':
        counter += 1
        i += 1
    initLength = counter
    funcName = t.value[1:initLength]
    counter += 1
    #get contents of parens
    while t.value[i] != ')':
        counter += 1
        i += 1

    funcVals = []
    temp = ""
    for i in t.value[initLength:counter]:
        if not (i == "," or i == "(" or i == ")"):
            temp += i
        elif not (temp == ""):
            funcVals.append(temp)
            temp = ""
        else:
            pass
    funcVals = extractVals(funcVals)
    funcCall = str(funcName) + "(" + str(funcVals) + ")"

    if funcName in funcList:
        eval(funcCall)
    else:
        print "This is not a valid function"
    return t

def t_CLSTRING(t):
    r'"[a-zA-Z0-9_+\*\- :,]*"'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lex.lex()

# BNF Parsing rules, "Grammar"
def p_program(p):
    '''program : declarations
               | functions
               | declarations functions'''
    print "Saw: ", p[1]

def p_functions(p):
    '''functions : function
                 | functions function'''

def p_function(p):
    '''function : type IDENTIFIER LPAREN RPAREN LCURLY RCURLY
                | type IDENTIFIER LPAREN RPAREN LCURLY declarations RCURLY
                | type IDENTIFIER LPAREN RPAREN LCURLY declarations statements RCURLY'''

def p_declarations(p):
    '''declarations : type idList SEMI
               | declarations type idList SEMI
               | type idList EQUALS expression SEMI
               | declarations type idList EQUALS expression SEMI'''
    if len(p)   == 4 : p[0] = p[2]
    elif len(p) == 5 : p[0] = p[3]
    elif len(p) == 6 : p[0] = p[2] + " = " + p[4]
    elif len(p) == 7 : p[0] = p[3] + " = " + p[5]
    print p[0]

def p_idList(p):
    '''idList : IDENTIFIER
              | IDENTIFIER COMMA idList'''
    if len(p) == 2: p[0] = p[1]
    else: p[0] = p[1] + ", " + p[3]

def p_type(p):
    '''type : INT
            | FLOAT
            | BOOL
            | LIST
            | TUPLE
            | OBJECT
            | STRING'''

def p_statements(p):
    '''statements : statement
                  | statements statement'''

def p_statement(p):
    '''statement : expression SEMI
                 | assignment SEMI
                 | whileStatement'''
    ##print "Saw a statement", p[1]

def p_assignment(p):
    '''assignment : IDENTIFIER EQUALS expression'''
    p[0] = "Assignment"
    tokenFlag = True
    opList = ['+', '/', '-', '*']
    try:
        for i in opList:
            # p[3][1] is the material to the right of "="
            if (i in p[3][1]):
                tokenFlag = False
        if (tokenFlag == True):
            if not isFloat(p[3][1]):
                variableDict[p[1]] = int(p[3][1])
            else:
                variableDict[p[1]] = float(p[3][1])
        else:
            evalList = []
            if (p[3][1][0] in variableDict) and (p[3][1][2:] in variableDict):
                evalList.append(variableDict[p[3][1][0]])
                evalList.append(p[3][1][1])
                evalList.append(variableDict[p[3][1][2:]])
            elif (p[3][1][0] in variableDict) and not (p[3][1][2:] in variableDict):
                evalList.append(variableDict[p[3][1][0]])
                evalList.append(p[3][1][1])
                evalList.append(p[3][1][2:])
            elif not (p[3][1][0] in variableDict) and (p[3][1][2:] in variableDict):
                evalList.append(p[3][1][0])
                evalList.append(p[3][1][1])
                evalList.append(variableDict[p[3][1][2:]])
            elif not (p[3][1][0] in variableDict) and not (p[3][1][2:] in variableDict):
                evalList.append(p[3][1][0])
                evalList.append(p[3][1][1])
                evalList.append(p[3][1][2:])
            else:
                print "ERROR: testfile.C syntax"
            variableDict[p[1]] = evalStr(evalList)
    except:
        pass

def p_while(p):
    '''whileStatement : WHILE LPAREN expression RPAREN LCURLY statements RCURLY'''
    p[0] = "While"

def p_expression(p):
    '''expression : conjunction
                  | conjunction OR_OP expression'''
    ##print p[1],"YYYYYYYYAYYYYYYYYYYYY"
    p[0] = "Expression: ", p[1]

def p_conjunction(p):
    '''conjunction : equality
                   | AND_OP equality'''
    ##print p[1],"BOOOOOOOOO"
    if len(p) == 4: p[0] = str(p[1]) + str(p[2]) + str(p[3])
    else : p[0] = str(p[1])

def p_equality(p):
    '''equality : relation
                | relation equOp equality'''
    #print p[1],"BOOOOOOOOO"
    if len(p) == 4: p[0] = str(p[1]) + str(p[2]) + str(p[3])
    else : p[0] = str(p[1])

def p_equOp(p):
    '''equOp : EQ_OP
             | NE_OP'''
    p[0] = p[1]

def p_relation(p):
    '''relation : addition
                | addition relOp relation'''
    if len(p) == 4: p[0] = str(p[1]) + str(p[2]) + str(p[3])
    else : p[0] = str(p[1])

def p_relOp(p):
    '''relOp : LT_OP
             | LE_OP
             | GT_OP
             | GE_OP'''
    p[0] = p[1]

def p_addition(p):
    '''addition : term
                | term addOP addition'''
    from java.lang import Math
    import Arithmetic
    if len(p) == 4 and isinstance( p[1], int ) and isinstance( p[3], int ):
        print "Calling java Arithmetic.add: ", Arithmetic.add(p[1], p[3])
    if len(p) == 4: p[0] = str(p[1]) + str(p[2]) + str(p[3])
    else : p[0] = p[1]

def p_addOP(p):
    '''addOP : PLUS
             | MINUS'''
    p[0] = p[1]

def p_term(p):
    '''term : factor
            | factor mulOP term'''
    if len(p) == 4: p[0] = str(p[1]) + str(p[2]) + str(p[3])
    else : p[0] = p[1]

def p_mulOP(p):
    '''mulOP : MULT
             | DIV
             | PRCNT'''
    p[0] = p[1]

def p_factor(p):
    '''factor : primary
              | primary unaryOP factor'''
    if len(p) == 4: p[0] = str(p[1]) + str(p[2]) + str(p[3])
    else : p[0] = p[1]

def p_unaryOp(p):
    '''unaryOP : MINUS
               | BANG'''
    p[0] = p[1]

def p_primary(p):
    '''primary : literal'''
    p[0] = p[1]

def p_literal(p):
    '''literal : INTEGER
               | IDENTIFIER
               | TRUE
               | FALSE
               | CLFLOAT
               | CLSTRING'''
    p[0] = p[1]

def p_functionCall(p):
    '''functionCall : FUNCTION_CALL SEMI'''
    #print "WE DID ITTTT"


def emptyline(self):
    """Do nothing on empty input line"""
    pass# Error handling rule

def p_error(p):
    print "At line: ", p.lexer.lineno,
    if p:
        pass
        #print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

with open('testfile.c', 'r') as content_file:
    content = content_file.read()
yacc.parse(content)

print variableDict