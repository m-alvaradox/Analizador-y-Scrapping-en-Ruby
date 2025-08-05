import ply.lex as lex
import datetime
import os
import sys

# Diccionario de palabras reservadas
reserved = {
    'bool': 'BOOL',
    'break': 'BREAK',
    'case': 'CASE',
    'char': 'CHAR',
    'class': 'CLASS',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'else': 'ELSE',
    'enum': 'ENUM',
    'float': 'FLOAT',
    'for': 'FOR',
    'foreach': 'FOREACH',
    'if': 'IF',
    'in': 'IN',
    'int': 'INT',
    'is': 'IS',
    'new': 'NEW',
    'null': 'NULL',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'public': 'PUBLIC',
    'return': 'RETURN',
    'static': 'STATIC',
    'string': 'STRING',
    'struct': 'STRUCT',
    'switch': 'SWITCH',
    'this': 'THIS',
    'void': 'VOID',
    'while': 'WHILE',
    'using': 'USING',
    'List': 'LIST', # por Mario Alvarado

}

special = {
    'Write': 'WRITE',
    'Read': 'READ',
    'WriteLine': 'WRITELINE',
    'Console': 'CONSOLE',
    'Main': 'MAIN',
    'args': 'ARGS',
    'Count': 'COUNT'
}

# Lista de tokens
tokens = [
    'IDENTIFICADOR',
    'NOMBRE_CLASE',
    'COMENTARIO_UNA_LINEA', # //

    # Valores: por Andres Layedra
    'VALOR_ENTERO',
    'VALOR_FLOTANTE',
    'VALOR_STRING',
    'VALOR_CHAR',
    'VALOR_HEXADECIMAL',       # Ej: 0x1F4
    'VALOR_BINARIO',      # Ej: 0b1010
    'VALOR_BOOLEANO',  # true o false

    # Operadores
    'MAS', 'MENOS', 'MULTIPLICACION', 'DIVISION',
    'MODULO', 'INCREMENTO', 'DECREMENTO',
    'ASIGNACION', 'MAS_ASIGNACION', 'MENOS_ASIGNACION',
    'MULTIPLICACION_ASIGNACION', 'DIVISION_ASIGNACION', 'MODULO_ASIGNACION',
    'IGUAL', 'NO_IGUAL', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL',
    'CONJUNCION', 'DISYUNCION', 'NEGACION',

    # Delimitadores
    'PARENTESIS_IZQ', 'PARENTESIS_DER', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    'COMA', 'PUNTO', 'PUNTO_COMA', 'DOS_PUNTOS',

] + list(reserved.values()) + list(special.values())

# Expresiones regulares para tokens simples

t_MAS = r'\+'
t_MENOS = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_MODULO = r'%'
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'

t_ASIGNACION = r'='
t_MAS_ASIGNACION = r'\+='
t_MENOS_ASIGNACION = r'-='
t_MULTIPLICACION_ASIGNACION = r'\*='
t_DIVISION_ASIGNACION = r'/='
t_MODULO_ASIGNACION = r'%='


t_IGUAL = r'=='
t_NO_IGUAL = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='

t_CONJUNCION = r'&&'
t_DISYUNCION = r'\|\|'
t_NEGACION = r'!'

t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'

t_COMA = r','
t_PUNTO = r'\.'
t_PUNTO_COMA = r';'
t_DOS_PUNTOS = r':'

# Reglas con acciones
expecting_class_name = False
clases_declaradas = set()

def t_VALOR_BOOLEANO(t):
    r'\b(true|false)\b'
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    global expecting_class_name

    if expecting_class_name:
        t.type = 'NOMBRE_CLASE'
        clases_declaradas.add(t.value) # Añadir a conjunto de clases declaradas
        expecting_class_name = False
    else:
        if t.value in special:
            t.type = special[t.value]
        else:
            t.type = reserved.get(t.value, 'IDENTIFICADOR')

    if t.value == 'class':
        expecting_class_name = True

    return t

def t_COMENTARIO_UNA_LINEA(t):
    r'//.*'
    return t

def t_VALOR_HEXADECIMAL(t):
    r'0[xX][0-9A-Fa-f]+'
    t.value = int(t.value, 16)
    return t

def t_VALOR_BINARIO(t):
    r'0[bB][01]+'
    t.value = int(t.value, 2)
    return t

def t_VALOR_FLOTANTE(t):
    r'\d+\.\d+([eE][+-]?\d+)?[fF]?'
    t.value = float(t.value.rstrip('fF'))
    return t

def t_VALOR_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_VALOR_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Elimina las comillas
    return t

def t_VALOR_CHAR(t):
    r"'([^'\\]|\\.)*'"
    if len(t.value) != 3:  # Debe ser un solo carácter entre comillas
        print(f"Error: Literal de carácter inválido '{t.value}' en la línea {t.lineno}")
        t.type = 'ERROR'
    else:
        t.value = t.value[1]  # Elimina las comillas
    return t



t_ignore = ' \t\r'

def t_COMENTARIO_MULTILINEA(t):
    r'/\*[\s\S]*?\*/'
    pass  # Ignora comentarios multilínea

# Regla para manejar nuevas líneas y actualizar el número de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para manejar errores de caracteres ilegales
def t_error(t):
    t.type = 'ERROR_LÉXICO!'
    t.value = t.value[0]
    t.lexer.skip(1)
    return t

# Construir el lexer
lexer = lex.lex()
