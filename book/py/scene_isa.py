#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Mario Mlačak, mmlacak@gmail.com
# Licensed under 3-clause (modified) BSD license. See LICENSE.txt for details.


from util import in_range
from piece import PieceType
from board import BoardType, Board
from mark import MarkType
from corner import Corner
from scene import Scene
from scene_mixin import SceneMixin

import gen_steps as GS


class SceneIsa(SceneMixin):

    # overrides
    def _get_recent_scene_method_names(self):
        return  [
                    'isa_one', \
                ]

    def setup_board(self, bt, name):
        bt = BoardType(bt)
        scene = Scene(name, bt)

        scene.board.setup()
        return scene

    def find_piece(self, scene, piece_type, search_light=True, search_queen_side=True):
        pos_0, pos_max = scene.board.get_position_limits() # ((0, 0), (w, h))

        # pos +1 and -1, because range() does not include end limit into iteration.
        i_start, i_end, i_diff = (pos_0[0], pos_max[0]+1, 1) if search_queen_side else (pos_max[0], pos_0[0]-1, -1)
        j = pos_0[1] if search_light else pos_max[1]

        pt = PieceType(piece_type)

        for i in range(i_start, i_end, i_diff):
            if scene.board.get_piece(i, j) == pt:
                return pt, i, j

        return None, None, None

    def check_field(self, scene, piece_type, i, j):
        pt = PieceType(piece_type)
        other = scene.board.get_piece(i, j)

        if pt.is_friend(other):
            return True
        elif pt.is_foe(other):
            return False
        else:
            return None # empty field

    def check_if_opponents_king(self, scene, piece_type, i, j):
        pt = PieceType(piece_type)
        other = scene.board.get_piece(i, j)

        if pt.is_foe(other) and other in [PieceType.King, -PieceType.King]:
            return True
        else:
            return False

    def traverse_pegasus_dir(self, scene, piece_type, i, j):
        assert piece_type in [-PieceType.Pegasus, PieceType.Pegasus]

        pt = PieceType(piece_type)
        start = (i, j)

        for index, rel in enumerate( GS.DEFAULT_KNIGHT_REL_MOVES ):
            current = start
            while scene.board.is_on_board(*current):
                next_ = GS.add(rel, current)

                check = self.check_field(scene, pt, *next_)
                if check is True:
                    # own piece encountered
                    break
                elif check is False:
                    # opponent's piece encountered
                    for i, r in enumerate( GS.DEFAULT_KNIGHT_REL_MOVES ):
                        c = GS.add(r, current)
                        if self.check_if_opponents_king(scene, pt, *c):
                            scene.append_text(str(i+1), *c, mark_type=MarkType.Illegal)
                            scene.append_field_marker(*c, mark_type=MarkType.Illegal)
                        else:
                            scene.append_text(str(i+1), *c, mark_type=MarkType.Legal)

                    if self.check_if_opponents_king(scene, pt, *next_):
                        scene.append_arrow( *(current + next_), mark_type=MarkType.Illegal )
                    else:
                        scene.append_arrow( *(current + next_), mark_type=MarkType.Action )

                    for i, r in enumerate( GS.DEFAULT_KNIGHT_REL_MOVES ):
                        c = GS.add(r, next_)
                        if self.check_if_opponents_king(scene, pt, *c):
                            scene.append_field_marker(*c, mark_type=MarkType.Illegal)
                        else:
                            scene.append_field_marker(*c, mark_type=MarkType.Action)

                    break
                else:
                    # empty field
                    if  scene.board.is_on_board(*next_):
                        scene.append_arrow( *(current + next_), mark_type=MarkType.Legal )

                current = next_

        yield scene

    def traverse_shaman_dir(self, scene, piece_type, i, j):
        assert piece_type in [-PieceType.Shaman, PieceType.Shaman]

        pt = PieceType(piece_type)
        start = (i, j)
        rel_moves = GS.DEFAULT_KNIGHT_REL_MOVES if pt.is_light() else GS.DEFAULT_UNICORN_REL_LONG_MOVES
        rel_capture = GS.DEFAULT_UNICORN_REL_LONG_MOVES if pt.is_light() else GS.DEFAULT_KNIGHT_REL_MOVES

        for index, rel in enumerate( rel_moves ):
            previous = current = start
            while scene.board.is_on_board(*current):
                next_ = GS.add(rel, current)

                check = self.check_field(scene, pt, *next_)
                if check is True:
                    # own piece encountered
                    break
                elif check is False:
                    # opponent's piece encountered
                    for i, r in enumerate( rel_capture ):
                        c = GS.add(r, previous)
                        if self.check_if_opponents_king(scene, pt, *c):
                            scene.append_text(str(i+1), *c, mark_type=MarkType.Illegal)
                            scene.append_field_marker(*c, mark_type=MarkType.Illegal)
                        else:
                            scene.append_text(str(i+1), *c, mark_type=MarkType.Legal)

                    for i, r in enumerate( rel_capture ):
                        c = current
                        while scene.board.is_on_board(*c):
                            n = GS.add(r, c)
                            if self.check_field(scene, pt, *n) is False:
                                if self.check_if_opponents_king(scene, pt, *n):
                                    scene.append_arrow( *(c + n), mark_type=MarkType.Illegal )
                                else:
                                    scene.append_arrow( *(c + n), mark_type=MarkType.Action )
                            else:
                                scene.append_field_marker(*n, mark_type=MarkType.Action)
                                break
                            c = n

                    break
                else:
                    # empty field
                    if  scene.board.is_on_board(*next_):
                        scene.append_arrow( *(current + next_), mark_type=MarkType.Legal )
                    elif (pt.is_dark() and current[1] < 5) or (pt.is_light() and current[1] > scene.board.get_height() - 5):
                        # close to opponent's initial positions
                        for i, r in enumerate( rel_capture ):
                            n = GS.add(r, previous)
                            if scene.board.is_on_board(*n):
                                if self.check_if_opponents_king(scene, pt, *n):
                                    scene.append_text(str(i+1), *n, mark_type=MarkType.Illegal)
                                else:
                                    scene.append_text(str(i+1), *n, mark_type=MarkType.Legal)

                        for i, r in enumerate( rel_capture ):
                            c = current
                            while scene.board.is_on_board(*c):
                                n = GS.add(r, c)
                                if self.check_field(scene, pt, *n) is False:
                                    if self.check_if_opponents_king(scene, pt, *n):
                                        scene.append_arrow( *(c + n), mark_type=MarkType.Illegal )
                                    else:
                                        scene.append_arrow( *(c + n), mark_type=MarkType.Action )
                                else:
                                    scene.append_field_marker(*n, mark_type=MarkType.Action)
                                    break
                                c = n

                previous = current
                current = next_

        yield scene

    def check_centaur_field(self, scene, piece_type, i, j):
        pt = PieceType(piece_type)
        return (pt.is_light() and scene.board.is_light(i, j)) or (pt.is_dark() and scene.board.is_dark(i, j))

    def check_centaur_rel_move(self, rel):
        if rel in GS.DEFAULT_UNICORN_REL_LONG_MOVES:
            return True
        elif rel in GS.DEFAULT_KNIGHT_REL_MOVES:
            return False
        else:
            return None

    def traverse_centaur_dir(self, scene, piece_type, i, j):
        assert piece_type in [-PieceType.Centaur, PieceType.Centaur]

        bt = scene.board.type
        fn = scene.file_name
        pt = PieceType(piece_type)
        start = (i, j)
        rel_moves = GS.DEFAULT_KNIGHT_REL_MOVES if self.check_centaur_field(scene, pt, i, j) else GS.DEFAULT_UNICORN_REL_LONG_MOVES
        rel_second = GS.DEFAULT_UNICORN_REL_LONG_MOVES if self.check_centaur_field(scene, pt, i, j) else GS.DEFAULT_KNIGHT_REL_MOVES

        for rel_1 in rel_moves:
            for rel_2 in rel_second:
                gen_func = GS.gen_items([rel_1, rel_2, ])
                current = start
                new_scene = self.setup_board(bt, fn)
                scene_has_content = False

                rel_previous = None
                for rel in gen_func():
                    next_ = GS.add(rel, current)
                    rel_current = GS.DEFAULT_UNICORN_REL_LONG_MOVES if self.check_centaur_rel_move(rel) else GS.DEFAULT_KNIGHT_REL_MOVES
                    rel_capture = GS.DEFAULT_KNIGHT_REL_MOVES if self.check_centaur_rel_move(rel) else GS.DEFAULT_UNICORN_REL_LONG_MOVES

                    if new_scene.board.is_on_board(*next_):
                        check = self.check_field(new_scene, pt, *next_)

                        if check is True:
                            # own piece encountered
                            scene_has_content = False
                            break
                        elif check is False:
                            # opponent's piece encountered
                            for i, r in enumerate( rel_current ):
                                c = GS.add(r, current)
                                if self.check_if_opponents_king(scene, pt, *c):
                                    new_scene.append_text(str(i+1), *c, mark_type=MarkType.Illegal)
                                    new_scene.append_field_marker(*c, mark_type=MarkType.Illegal)
                                else:
                                    new_scene.append_text(str(i+1), *c, mark_type=MarkType.Legal)

                            if self.check_if_opponents_king(scene, pt, *next_):
                                new_scene.append_arrow( *(current + next_), mark_type=MarkType.Illegal )
                            else:
                                new_scene.append_arrow( *(current + next_), mark_type=MarkType.Action )

                            for i, r in enumerate( rel_capture ):
                                c = GS.add(r, next_)
                                if self.check_if_opponents_king(scene, pt, *c):
                                    new_scene.append_field_marker(*c, mark_type=MarkType.Illegal)
                                else:
                                    new_scene.append_field_marker(*c, mark_type=MarkType.Action)

                            scene_has_content = True
                            break
                        else:
                            # empty field
                            new_scene.append_arrow( *(current + next_), mark_type=MarkType.Legal )
                            scene_has_content = True
                    else:
                        diff = 2 + 4 if self.check_centaur_rel_move(rel) else 2 + 1 # 2 default ranks (figures + Pawns) + max vertical step + 1 for strict check
                        if (pt.is_dark() and current[1] < diff) or (pt.is_light() and current[1] > scene.board.get_height() - diff):
                            # close to opponent's initial positions
                            if rel_previous is not None:
                                prev = GS.sub(current, rel_previous)
                                for i, r in enumerate( rel_capture ):
                                    c = GS.add(r, prev)
                                    if self.check_if_opponents_king(scene, pt, *c):
                                        new_scene.append_text(str(i+1), *c, mark_type=MarkType.Illegal)
                                        new_scene.append_field_marker(*c, mark_type=MarkType.Illegal)
                                    else:
                                        new_scene.append_text(str(i+1), *c, mark_type=MarkType.Legal)

                            for i, r in enumerate( rel_current ):
                                c = GS.add(r, current)
                                if self.check_if_opponents_king(scene, pt, *c):
                                    new_scene.append_field_marker(*c, mark_type=MarkType.Illegal)
                                else:
                                    new_scene.append_field_marker(*c, mark_type=MarkType.Action)
                            scene_has_content = True
                        else:
                            scene_has_content = False
                        break

                    rel_previous = rel
                    current = next_

                if scene_has_content:
                    yield new_scene

    def get_traverse_func(self, piece_type):
        dct =   {
                    PieceType.Pegasus: self.traverse_pegasus_dir, \
                    -PieceType.Pegasus: self.traverse_pegasus_dir, \
                    PieceType.Shaman: self.traverse_shaman_dir, \
                    -PieceType.Shaman: self.traverse_shaman_dir, \
                    PieceType.Centaur: self.traverse_centaur_dir, \
                    -PieceType.Centaur: self.traverse_centaur_dir, \
                }
        if piece_type in dct:
            return dct[ piece_type ]
        else:
            return None

    def isa_one(self, board_types=None):
        bts = board_types if board_types is not None else BoardType.iter(include_odd=True)
        for index, bt in enumerate( bts ):
#             for pt in [PieceType.Centaur, ]:
            for pt in [PieceType.Pegasus, PieceType.Shaman, PieceType.Centaur, ]:
                for sl in [True, False]:
                    for sqs in [True, False]:
                        scene = self.setup_board(bt, 'isa')

                        pos_G = self.find_piece(scene, pt, search_light=sl, search_queen_side=sqs)
                        if pos_G != (None, None, None):
                            print(pos_G)

                            for idx, new_scene in enumerate( self.get_traverse_func(pos_G[0])(scene, *pos_G) ):
                                new_scene.file_name = '%s_%02d_%s_%02d' % (bt.get_label(), index, PieceType(pos_G[0]).get_label(), idx)
                                yield new_scene
