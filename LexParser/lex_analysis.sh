#!/bin/bash


flex lexer.l


bison -Wcounterexamples  -d parser.y
#bison   -d parser.y


#gcc lexer.o parser.o -o parser -lfl 

gcc lex.yy.c parser.tab.c -o parser
export YYDEBUG=1
./parser  < test_file_1.gst
./parser  < test_file_2.gst
./parser  < test_file_3.gst

# Remoção de arquivos temporários
#rm -rf lex.yy.c parser.tab.c parser.tab.h lexer.o parser.o
