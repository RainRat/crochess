.. Copyright (c) 2025 Mario Mlačak, mmlacak@gmail.com
   This text is Public Domain work, under CC0 1.0 Universal Public Domain Dedication. See accompanying LICENSING, COPYING files for details.
   Included source code files are licensed under GNU GPL v3+ license. See LICENSING, COPYING files in root folder of the project for details.

.. include:: ../defines.rst

.. _lbl-libcc-ccparseply:

Parse ply
=========

Documents ``cc_parse_ply.h`` and ``cc_parse_ply.c`` files,
which contain various parse ply definitions and functions.

.. _lbl-libcc-ccparseply-functions:

Functions
---------

.. c:function:: bool cc_parse_plies( char const * move_an, bool is_turn_light, cc_uint_t board_size, CcPly ** plies__o, CcParseMsg ** parse_msgs__iod )

    Function parses all plies in a given move notation, results are returned via
    output parameters, if successful; otherwise, just messages from parser.

    :param move_an: Move notation; null-terminated, :term:`AN` string.
    :param is_turn_light: Flag, whether it's light player turn, or dark one's.
    :param board_size: Size of a chessboard being played.
    :param plies__o: _Output_, parsed plies.
    :param parse_msgs__iod: *Optional* *input/output* parameter, linked list.
    :returns: :c:data:`true` if successful, :c:data:`false` otherwise.

.. _lbl-libcc-ccparseply-sourcecodeheader:

Header file
-----------

Included source header file is ``cc_parse_ply.h``.

.. literalinclude:: ../../../ws/libcrochess/inc/cc_parse_ply.h
    :language: C
    :linenos:

.. _lbl-libcc-ccparseply-sourcecodefile:

Source code file
----------------

Included source code file is ``cc_parse_ply.c``.

.. literalinclude:: ../../../ws/libcrochess/src/cc_parse_ply.c
    :language: C
    :linenos:
