#ifndef TOKENS_H
#define TOKENS_H

// Definindo os valores dos tokens
#define IF 257
#define ELSE 258
#define FOREACH 259
#define TO 260
#define WHILE 261
#define SHOW 262
#define RULE 263
#define MATCH 264
#define SCANHOST 265
#define TRAFFIC_INFORMATION 266
#define INPUT 267
#define INT 268
#define STR 269
#define LPAREN 270
#define RPAREN 271
#define LBRACE 272
#define RBRACE 273
#define COMMA 274
#define SEMICOLON 275
#define EQ 276
#define GT 277
#define LT 278
#define AND 279
#define OR 280
#define PLUS 281
#define MINUS 282
#define TIMES 283
#define DIVIDE 284
#define ASSIGN 285
#define NOT 286
#define NUMBER 287
#define IDENTIFIER 288
#define STRING 289
#define UNKNOWN_CHARACTER 290
#define NEWLINE 291
#define DECLARE 292


extern char* yyval; // Agora yyval é um ponteiro para char

#endif /* TOKENS_H */
