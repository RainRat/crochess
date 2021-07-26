// Copyright (c) 2021 Mario Mlačak, mmlacak@gmail.com
// Licensed under 3-clause (modified) BSD license. See LICENSE for details.

#ifndef __CC_PARSER_H__
#define __CC_PARSER_H__

#include <stdbool.h>

typedef enum CcParseMsgEnum
{
    CC_PME_Debug,
    CC_PME_Info,
    CC_PME_Warning,
    CC_PME_Error,
    CC_PME_Fatal,
} CcParseMsgEnum;

typedef struct CcParseMsg
{
    CcParseMsgEnum type;
    size_t pos;
    char const * msg;
    struct CcParseMsg * next;
} CcParseMsg;

CcParseMsg * cc_parse_msg_new( CcParseMsgEnum type,
                               size_t pos,
                               char const * const restrict msg );

CcParseMsg * cc_parse_msg_append_new( CcParseMsg * const restrict parse_msgs,
                                      CcParseMsgEnum type,
                                      size_t pos,
                                      char const * const restrict msg );

CcParseMsg * cc_parse_msg_init_or_append_new( CcParseMsg ** const restrict parse_msgs,
                                              CcParseMsgEnum type,
                                              size_t pos,
                                              char const * const restrict msg );

bool cc_parse_msg_free_all( CcParseMsg ** const restrict parse_msgs_f );


char * cc_parse_next_ply_str_new( char const * const restrict move_str_s,
                                  CcParseMsg ** parse_msgs );

#endif /* __CC_PARSER_H__ */
