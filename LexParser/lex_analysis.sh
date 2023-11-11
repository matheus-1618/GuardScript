#!/bin/bash

# Compilação do lexer
flex lexer.l

# Compilação do código C gerado
gcc lex.yy.c -o lexer -lfl

# Execução do lexer
./lexer < test_file.gs

rm -rf lex.yy.c