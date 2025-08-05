# analizador.py
from lex import lexer, tokens, clases_declaradas
from yacc import parser, errores as errores_sintacticos
import datetime
import os
import ply.lex as lex
import ply.yacc as yacc

def analisis_lexico(codigo):
    lexer.input(codigo)
    resultado = []
    for tok in lexer:
        resultado.append(f"{tok.type:15} -> {tok.value}")
    return "\n".join(resultado)

def analisis_sintactico(codigo):
    errores_sintacticos.clear()
    lexer.lineno = 1
    parser.parse(codigo, lexer=lexer)
    if errores_sintacticos:
        return "\n".join(errores_sintacticos)
    return "Análisis realizado correctamente."

def analisis_semantico(codigo):
    lexer.lineno = 1 
    lexer.input(codigo)
    tokens_extraidos = list(lexer)

    variables_declaradas = set()
    tipos_variables = {}
    usos_variables = set()
    clases_usadas = set()
    metodos_definidos = {"Add":"bool"}
    metodos_llamados = []

    errores_semanticos = []

    i = 0
    while i < len(tokens_extraidos):
        token = tokens_extraidos[i]
        prev = tokens_extraidos[i - 1] if i > 0 else None
        next_ = tokens_extraidos[i + 1] if i < len(tokens_extraidos) - 1 else None

        # ========================
        # Reglas Semánticas
        # Por Mario Alvarado
        # ========================

 # Ejemplo: foreach (int x in miLista) { ... }
        if token.type == "FOREACH":
            tipo_iterador = tokens_extraidos[i + 2] if i + 2 < len(tokens_extraidos) else None
            var_iterador = tokens_extraidos[i + 3] if i + 3 < len(tokens_extraidos) else None
            in_token = tokens_extraidos[i + 4] if i + 4 < len(tokens_extraidos) else None
            lista_token = tokens_extraidos[i + 5] if i + 5 < len(tokens_extraidos) else None

            if not (tipo_iterador and var_iterador and in_token and lista_token):
                errores_semanticos.append(
                    f"[ERROR SEMÁNTICO] Línea {token.lineno}: Sintaxis incompleta en foreach."
                )
            elif lista_token.value not in tipos_variables or not tipos_variables[lista_token.value].startswith("LIST"):
                errores_semanticos.append(
                    f"[ERROR SEMÁNTICO] Línea {lista_token.lineno}: La variable '{lista_token.value}' no es una lista declarada."
                )
            else:
                tipo_lista = tipos_variables[lista_token.value][5:-1]  # Extrae el tipo entre <>
                if tipo_iterador.type != tipo_lista.upper():
                    errores_semanticos.append(
                        f"[ERROR SEMÁNTICO] Línea {tipo_iterador.lineno}: "
                        f"Tipo de iterador '{tipo_iterador.type}' no coincide con el tipo de la lista '{tipo_lista.upper()}'."
                    )

        # Declaración de lista: List<T> nombre = new List<T> { ... };
        if token.type == "LIST" and next_ and next_.type == "MENOR":
            # Buscar el tipo de la lista
            tipo_lista = tokens_extraidos[i + 2] if i + 2 < len(tokens_extraidos) else None
            nombre_lista = tokens_extraidos[i + 4] if i + 4 < len(tokens_extraidos) else None
            if nombre_lista and nombre_lista.type == "IDENTIFICADOR":
                variables_declaradas.add(nombre_lista.value)
                tipos_variables[nombre_lista.value] = f"LIST<{tipo_lista.value}>"

        # Uso de lista sin declarar
        if token.type == "IDENTIFICADOR" and token.value in tipos_variables and tipos_variables[token.value].startswith("LIST"):
            # Ejemplo: miLista.Add(5);
            if next_ and next_.type == "PUNTO":
                metodo_lista = tokens_extraidos[i + 2] if i + 2 < len(tokens_extraidos) else None
                if metodo_lista and metodo_lista.type == "IDENTIFICADOR" and metodo_lista.value == "Add":
                    # Buscar el valor que se intenta agregar
                    if i + 5 < len(tokens_extraidos) and tokens_extraidos[i + 3].type == "PARENTESIS_IZQ":
                        valor_agregado = tokens_extraidos[i + 4]
                        tipo_lista = tipos_variables[token.value][5:-1]  # Extrae el tipo entre <>
                        tipo_valor_agregado = tipo_valor(valor_agregado)
                        if tipo_valor_agregado and tipo_valor_agregado != tipo_lista.upper():
                            errores_semanticos.append(
                                f"[ERROR SEMÁNTICO] Línea {valor_agregado.lineno}: "
                                f"Tipo incompatible en lista '{token.value}'. Se esperaba '{tipo_lista.upper()}', "
                                f"pero se intentó agregar '{tipo_valor_agregado}'."
                            )        


        # 1. Declaración de variable

        if token.type == "IDENTIFICADOR":
            usos_variables.add(token.value)

            if prev and prev.type in {"INT", "FLOAT", "STRING", "CHAR", "BOOL", "IDENTIFICADOR"}:
                # 2. Doble declaración
                if token.value in variables_declaradas:
                    errores_semanticos.append(
                        f"[ERROR SEMÁNTICO] Línea {token.lineno}: Variable '{token.value}' ya fue declarada."
                    )
                else:
                    variables_declaradas.add(token.value)
                    tipos_variables[token.value] = prev.type

            # 3. Uso sin declaración
            elif next_ and next_.type == "ASIGNACION":
                if token.value not in variables_declaradas:
                    errores_semanticos.append(
                        f"[ERROR SEMÁNTICO] Línea {token.lineno}: Variable '{token.value}' usada sin ser declarada."
                    )
                else:
                    # 4. Asignación con tipo incompatible
                    valor = tokens_extraidos[i + 2] if i + 2 < len(tokens_extraidos) else None
                    tipo_esperado = tipos_variables[token.value]
                    tipo_asignado = tipo_valor(valor)

                    if tipo_asignado and tipo_esperado != tipo_asignado:
                        errores_semanticos.append(
                            f"[ERROR SEMÁNTICO] Línea {token.lineno}: Asignación incompatible. "
                            f"Se esperaba '{tipo_esperado}', pero se asignó '{tipo_asignado}'."
                        )
                       
        # ========================
        # Reglas Semánticas
        # Por Andres Layedra
        # ======================== 

        # 5. División por cero
        if token.type == "DIVISION":
            siguiente = tokens_extraidos[i + 1] if i + 1 < len(tokens_extraidos) else None
            if siguiente and siguiente.type == "VALOR_ENTERO" and siguiente.value == 0:
                errores_semanticos.append(
                    f"[ERROR SEMÁNTICO] Línea {token.lineno}: División por cero detectada."
                )

        # 6. Instancia de clase no declarada
        if token.type == "NEW":
            siguiente = tokens_extraidos[i + 1] if i + 1 < len(tokens_extraidos) else None
            if siguiente and siguiente.type == "IDENTIFICADOR":
                if siguiente.value not in clases_declaradas:
                    errores_semanticos.append(
                        f"[ERROR SEMÁNTICO] Línea {siguiente.lineno}: Clase '{siguiente.value}' no declarada."
                    )
                clases_usadas.add(siguiente.value)

        # ========================
        # Reglas Semánticas
        # Por Medardo Moran
        # ======================== 

        # 7. Registro de métodos definidos
        if token.type == "IDENTIFICADOR" and next_ and next_.type == "PARENTESIS_IZQ":
            # Verifica si es definición de método
            tipo_antes = tokens_extraidos[i - 1] if i > 0 else None
            if tipo_antes and tipo_antes.type in {"INT", "FLOAT", "STRING", "CHAR", "BOOL", "VOID"}:
                num_params = contar_parametros(tokens_extraidos, i + 2)
                metodos_definidos[token.value] = num_params

        # 8. Registro de llamadas a métodos (Ignorar llamadas a constructores new Clase())
        if token.type == "IDENTIFICADOR" and next_ and next_.type == "PARENTESIS_IZQ":
            prev_2 = tokens_extraidos[i - 1] if i > 0 else None
            if prev_2 and prev_2.type == "NEW":
                # Es constructor, no se registra como método normal
                pass
            else:
                if token.value not in metodos_definidos:
                    num_args = contar_parametros(tokens_extraidos, i + 2)
                    metodos_llamados.append((token.value, num_args, token.lineno))

        i += 1

    # 10. Verificar métodos inexistentes o mal llamados
    for nombre, num_args, linea in metodos_llamados:
        if nombre not in metodos_definidos:
            errores_semanticos.append(
                f"[ERROR SEMÁNTICO] Línea {linea}: Método '{nombre}' no está definido."
            )    
        elif metodos_definidos[nombre] != num_args:
            errores_semanticos.append(
                f"[ERROR SEMÁNTICO] Línea {linea}: Método '{nombre}' llamado con {num_args} argumento(s), "
                f"pero se esperaban {metodos_definidos[nombre]}."
            )

    if errores_semanticos:
        return "\n".join(errores_semanticos)
    return "Análisis realizado correctamente."

def tipo_valor(token):
    if not token:
        return None
    if token.type == "VALOR_ENTERO":
        return "INT"
    elif token.type == "VALOR_FLOTANTE":
        return "FLOAT"
    elif token.type == "VALOR_STRING":
        return "STRING"
    elif token.type == "VALOR_CHAR":
        return "CHAR"
    elif token.type == "VALOR_BOOLEANO":
        return "BOOL"
    elif token.type == "VALOR_HEXADECIMAL":
        return "INT"
    elif token.type == "VALOR_BINARIO":
        return "INT"
    return None  # Desconocido o expresión compleja

def contar_parametros(tokens, start_idx):
    count = 0
    profundidad = 1
    i = start_idx
    esperando_valor = True

    while i < len(tokens):
        t = tokens[i]
        if t.type == "PARENTESIS_DER":
            profundidad -= 1
            if profundidad == 0:
                break
        elif t.type == "PARENTESIS_IZQ":
            profundidad += 1
        elif t.type == "COMA" and profundidad == 1:
            count += 1
            esperando_valor = True
        elif esperando_valor and t.type.startswith("VALOR_") or t.type == "IDENTIFICADOR":
            count += 1
            esperando_valor = False
        i += 1
    return count
