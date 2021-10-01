// Copyright (c) 2021 Mario Mlačak, mmlacak@gmail.com
// Licensed under GNU GPL v3+ license. See LICENSE, COPYING files for details.

#ifndef __CC_PARSE_MOVE_H__
#define __CC_PARSE_MOVE_H__

#include "cc_chessboard.h"

// #include "cc_step.h"
#include "cc_ply.h"
#include "cc_move.h"

#include "cc_parse_msg.h"


// DOCS
CcPly * cc_parse_ply( char const * const restrict ply_str,
                      CcChessboard const * const restrict cb,
                      CcParseMsg ** parse_msgs_io );

// DOCS
CcMove * cc_parse_move( char const * const restrict move_str,
                        CcChessboard const * const restrict cb,
                        CcParseMsg ** parse_msgs_io );


#endif /* __CC_PARSE_MOVE_H__ */
