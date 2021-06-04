// Copyright (c) 2021 Mario Mlačak, mmlacak@gmail.com
// Licensed under 3-clause (modified) BSD license. See LICENSE for details.

#ifndef __TOKENIZER_H__
#define __TOKENIZER_H__

#include <stddef.h>

extern char const TOKEN_SEPARATORS_WHITEPSACE[];
extern char const TOKEN_SEPARATORS_PUNCTUATION[];


bool char_in( char c, char const * const restrict seps );

char const * traverse_chars( char const * const restrict pos,
                             char const * const restrict seps,
                             bool skip_or_stop_at );

char const * skip_chars( char const * const restrict pos, char const * const restrict seps );
char const * stop_at_chars( char const * const restrict pos, char const * const restrict seps );


char * next_token_new( char const * const restrict str /* = NULL */,
                       char const * const restrict seps /* = NULL */ );

char * str_trim_new( char const * const restrict str, char const * const restrict chars );

// size_t flush_stdin();

#endif /* __TOKENIZER_H__ */
