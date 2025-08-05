import ply.yacc as yacc
import datetime
import os
import sys
from lex import tokens  

# Variables para logs y errores
errores = []

# Reglas de precedencia
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'MODULO'),
    ('right', 'NEGACION'),
)

# Inicio del análisis
def p_programa(p):
    '''programa : using_directivas clases'''
    p[0] = ("programa", p[1], p[2])

def p_using_directivas(p):
    '''using_directivas : using_directiva
                        | using_directiva using_directivas'''
    pass

def p_using_directiva(p):
    '''using_directiva : USING namespace PUNTO_COMA'''

def p_namespace(p):
    '''namespace : IDENTIFICADOR
                 | IDENTIFICADOR PUNTO namespace'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_clases(p):
    '''clases : clase
              | clase clases'''
    pass

# ========================
# Reglas de Estructuras de Datos: class
# Por Medardo Moran
# ========================
    
def p_clase(p):
    '''clase : PUBLIC CLASS NOMBRE_CLASE LLAVE_IZQ miembros_clase LLAVE_DER'''
    pass

def p_miembros_clase(p):
    '''miembros_clase : miembro_clase
                      | miembro_clase miembros_clase'''
    pass

def p_miembro_clase(p):
    '''miembro_clase : declaracion_variable
                     | metodo
                     | declaracion_struct
                     | declaracion_enum'''
    pass

# ========================
# Reglas de Estructuras de Datos: ENUM y STRUCT
# Por Andres Layedra
# ========================

def p_declaracion_struct(p):
    '''declaracion_struct : modificador STRUCT IDENTIFICADOR LLAVE_IZQ struct_miembros LLAVE_DER
                          | STRUCT IDENTIFICADOR LLAVE_IZQ struct_miembros LLAVE_DER'''
    pass 
       
def p_struct_miembros(p):
    '''struct_miembros : declaracion_variable
                       | declaracion_variable struct_miembros
                       | constructor_struct'''
    pass

def p_constructor_struct(p):
    '''constructor_struct : PUBLIC IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER'''
    pass

def p_declaracion_enum(p):
    '''declaracion_enum : modificador ENUM IDENTIFICADOR LLAVE_IZQ enumeradores LLAVE_DER
                        | ENUM IDENTIFICADOR LLAVE_IZQ enumeradores LLAVE_DER'''
    pass

def p_enumeradores(p):
    '''enumeradores : IDENTIFICADOR
                    | IDENTIFICADOR COMA enumeradores'''
    pass

# ========================
# Reglas de Estructuras de Datos: LIST
# Por Mario Alvarado
# ========================

def p_declaracion_lista(p):
    '''declaracion_lista : LIST MENOR tipo MAYOR IDENTIFICADOR ASIGNACION NEW LIST MENOR tipo MAYOR LLAVE_IZQ argumentos LLAVE_DER PUNTO_COMA
                         | LIST MENOR tipo MAYOR IDENTIFICADOR ASIGNACION NEW LIST MENOR tipo MAYOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''

# ========================
# Reglas de Declaración de Variables y Métodos

def p_declaracion_variable(p):
    '''declaracion_variable : tipo IDENTIFICADOR PUNTO_COMA
                            | tipo IDENTIFICADOR ASIGNACION expresion PUNTO_COMA
                            | tipo IDENTIFICADOR ASIGNACION llamada_funcion PUNTO_COMA
                            | tipo IDENTIFICADOR ASIGNACION NEW IDENTIFICADOR PARENTESIS_IZQ argumentos_opcional PARENTESIS_DER PUNTO_COMA
                            | declaracion_lista'''
    pass


def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | STRING
            | CHAR
            | BOOL
            | IDENTIFICADOR'''  # Para tipos definidos por el usuario
    pass

def p_metodo(p):
    '''metodo : modificador tipo IDENTIFICADOR PARENTESIS_IZQ parametros_opcional PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER
              | modificador VOID IDENTIFICADOR PARENTESIS_IZQ parametros_opcional PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER
              | PUBLIC STATIC VOID MAIN PARENTESIS_IZQ STRING CORCHETE_IZQ CORCHETE_DER ARGS PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER
              | PUBLIC STATIC VOID MAIN PARENTESIS_IZQ PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER'''
    pass

def p_modificador(p):
    '''modificador : PUBLIC
                    | PRIVATE
                    | PROTECTED'''
    pass

def p_parametros_opcional(p):
    '''parametros_opcional : parametros
                           | empty'''
    pass

def p_parametros(p):
    '''parametros : tipo IDENTIFICADOR
                  | tipo IDENTIFICADOR COMA parametros'''
    pass

def p_cuerpo(p):
    '''cuerpo : sentencia
              | sentencia cuerpo'''
    pass

def p_sentencia(p):
    '''sentencia : declaracion_variable
                 | declaracion_struct
                 | llamada_funcion PUNTO_COMA
                 | asignacion
                 | sentencia_if
                 | sentencia_for
                 | sentencia_foreach
                 | sentencia_switch
                 | sentencia_return
                 | sentencia_break
                 | sentencia_continue
                 | sentencia_console_write
                 | sentencia_console_read'''
    pass

def p_llamada_funcion(p):
    '''llamada_funcion : IDENTIFICADOR PARENTESIS_IZQ argumentos_opcional PARENTESIS_DER
                       | IDENTIFICADOR PUNTO IDENTIFICADOR PARENTESIS_IZQ argumentos_opcional PARENTESIS_DER
                       | IDENTIFICADOR PUNTO COUNT'''
    pass

def p_argumentos_opcional(p):
    '''argumentos_opcional : argumentos
                          | empty'''
    pass

def p_argumentos(p):
    '''argumentos : expresion
                  | expresion COMA argumentos'''
    pass

def p_asignacion(p):
    '''asignacion : IDENTIFICADOR ASIGNACION expresion PUNTO_COMA
                  | IDENTIFICADOR MAS_ASIGNACION expresion PUNTO_COMA 
                  | IDENTIFICADOR PUNTO IDENTIFICADOR ASIGNACION expresion PUNTO_COMA'''
    pass

def p_expresion(p):
    '''expresion : VALOR_ENTERO
                 | VALOR_FLOTANTE
                 | VALOR_STRING
                 | VALOR_CHAR
                 | VALOR_HEXADECIMAL
                 | VALOR_BINARIO
                 | VALOR_BOOLEANO
                 | IDENTIFICADOR
                 | llamada_funcion
                 | expresion operador expresion
                 | PARENTESIS_IZQ expresion PARENTESIS_DER'''
    pass

def p_operador(p):
    '''operador : MAS
                | MENOS
                | MULTIPLICACION
                | DIVISION
                | MODULO
                | MAYOR
                | MENOR
                | MAYOR_IGUAL
                | MENOR_IGUAL
                | IGUAL
                | NO_IGUAL
                | CONJUNCION
                | DISYUNCION'''
    pass

# ========================
# Reglas de Estructuras de Control: IF
# Por Mario Alvarado
# ========================

def p_sentencia_if(p):
    '''sentencia_if : IF PARENTESIS_IZQ expresion PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER
                    | IF PARENTESIS_IZQ expresion PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER ELSE LLAVE_IZQ cuerpo LLAVE_DER'''
    pass

# ========================
# Reglas de Estructuras de Control: FOR
# Por Medardo Moran
# ========================

def p_sentencia_for(p):
    '''sentencia_for : FOR PARENTESIS_IZQ declaracion_variable expresion PUNTO_COMA actualizacion PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER
                     | FOR PARENTESIS_IZQ expresion PUNTO_COMA actualizacion PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER
                     | FOR PARENTESIS_IZQ PUNTO_COMA expresion PUNTO_COMA actualizacion PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER'''
    pass

def p_sentencia_foreach(p):
    '''sentencia_foreach : FOREACH PARENTESIS_IZQ tipo IDENTIFICADOR IN IDENTIFICADOR PARENTESIS_DER LLAVE_IZQ cuerpo LLAVE_DER'''
    pass

def p_actualizacion(p):
    '''actualizacion : IDENTIFICADOR INCREMENTO
                     | IDENTIFICADOR DECREMENTO'''
    pass

# ========================
# Reglas de Estructuras de Control: SWITCH
# Por Andres Layedra
# ========================

def p_sentencia_switch(p):
    '''sentencia_switch : SWITCH PARENTESIS_IZQ expresion PARENTESIS_DER LLAVE_IZQ casos_switch LLAVE_DER'''
    pass

def p_casos_switch(p):
    '''casos_switch : caso_switch
                    | caso_switch casos_switch'''
    pass

def p_caso_switch(p):
    '''caso_switch : CASE VALOR_ENTERO DOS_PUNTOS cuerpo
                   | CASE VALOR_STRING DOS_PUNTOS cuerpo
                   | DEFAULT DOS_PUNTOS cuerpo'''
    pass

def p_sentencia_return(p):
    '''sentencia_return : RETURN expresion PUNTO_COMA
                        | RETURN PUNTO_COMA'''
    pass

def p_sentencia_break(p):
    '''sentencia_break : BREAK PUNTO_COMA'''
    pass


def p_sentencia_continue(p):
    '''sentencia_continue : CONTINUE PUNTO_COMA'''
    pass

def p_sentencia_console_write(p):
    '''sentencia_console_write : CONSOLE PUNTO WRITE PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA
                               | CONSOLE PUNTO WRITELINE PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA'''
    pass

def p_sentencia_console_read(p):
    '''sentencia_console_read : CONSOLE PUNTO READ PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''
    pass
      
def p_empty(p):
    'empty :'
    pass

# Manejo de errores sintácticos
def p_error(p):
    if p:
        errores.append(f"[ERROR SINTÁCTICO] Token inesperado: '{p.value}' en la línea {p.lineno}")
    else:
        errores.append("[ERROR SINTÁCTICO] Fin de archivo inesperado")

# Construcción del parser
parser = yacc.yacc()