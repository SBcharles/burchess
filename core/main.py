from abc import ABC, abstractmethod
import pydantic
from pydantic import BaseModel
from enum import Enum
from typing import List, Tuple, Optional
import math


class Rank(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


class File(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'


class Colour(str, Enum):
    BLACK = 'Black'
    WHITE = 'White'


class Square(BaseModel):
    rank: Rank
    file: File
    colour: Colour


def square_colour(rank: Rank, file: File) -> Colour:
    file_num = list(File).index(file) + 1
    rank_num = rank.value
    #  chessboard squares are black if rank and file are both odd, or both even.
    return Colour.BLACK if (file_num % 2 == rank_num % 2) else Colour.WHITE


def create_all_squares() -> List[Square]:
    squares = [
        Square(file=file, rank=rank, colour=square_colour(rank, file))
        for rank in Rank for file in File
    ]
    return squares


class MovementAbility(BaseModel):
    max_units: int
    direction: Tuple[int, int]
    circumstance: Optional[str]  # e.g. 'PAWN_IS_CAPTURING'


class Piece(ABC, BaseModel):
    colour: Colour

    @abstractmethod
    def move_abilities(self) -> List:
        raise NotImplementedError


def point_generator(num_points: int, starting_theta: float) -> List[Tuple[int, int]]:
    """ Maybe excessive code. Generates direction tuples, saving having to hard code each Piece's move_abilities"""
    points = []
    theta = starting_theta
    if num_points == 8 and starting_theta == math.pi / 6:
        knight_cheat_factor = 2
    else:
        knight_cheat_factor = 1
    while theta < 2*math.pi:
        x = round(knight_cheat_factor * math.cos(theta))
        y = round(knight_cheat_factor * math.sin(theta))
        points.append((x, y))
        theta += 2 * math.pi / num_points
    return points


class King(Piece):
    def move_abilities(self) -> List:
        abilities = [MovementAbility(max_units=1, direction=point) for point in point_generator(8, 0)]
        return abilities


class Queen(Piece):
    def move_abilities(self) -> List:
        abilities = [MovementAbility(max_units=7, direction=point) for point in point_generator(8, 0)]
        return abilities


class Bishop(Piece):
    def move_abilities(self) -> List:
        abilities = [MovementAbility(max_units=7, direction=point) for point in point_generator(4, math.pi / 4)]
        return abilities


class Rook(Piece):
    def move_abilities(self) -> List:
        abilities = [MovementAbility(max_units=7, direction=point) for point in point_generator(4, 0)]
        return abilities


class Knight(Piece):
    def move_abilities(self) -> List:
        abilities = [MovementAbility(max_units=1, direction=point) for point in point_generator(8, math.pi / 6)]
        return abilities


class WhitePawn(Piece):  # Todo consideration! black pawns move in negative y direction.
    colour = Colour.WHITE
    def move_abilities(self) -> List:
        abilities = []
        abilities.append(MovementAbility(max_units=1, direction=(0, 1)))
        abilities.append(MovementAbility(max_units=1, direction=(0, 1), circumstance="STARTING POSITION"))  # Todo does max_units concept work here?
        abilities.append(MovementAbility(max_units=1, direction=(1, 1), circumstance="PIECE_CAPTURE"))
        abilities.append(MovementAbility(max_units=1, direction=(-1, 1), circumstance="PIECE_CAPTURE"))
        abilities.append(MovementAbility(max_units=1, direction=(1, 1), circumstance="EN_PASSANT"))
        abilities.append(MovementAbility(max_units=1, direction=(-1, 1), circumstance="EN_PASSANT"))
        return abilities


class BlackPawn(Piece):
    colour = Colour.BLACK
    def move_abilities(self) -> List:
        abilities = []
        abilities.append(MovementAbility(max_units=1, direction=(0, -1)))
        abilities.append(MovementAbility(max_units=1, direction=(0, -1), circumstance="STARTING POSITION"))
        abilities.append(MovementAbility(max_units=1, direction=(1, -1), circumstance="PIECE_CAPTURE"))
        abilities.append(MovementAbility(max_units=1, direction=(-1, -1), circumstance="PIECE_CAPTURE"))
        abilities.append(MovementAbility(max_units=1, direction=(1, -1), circumstance="EN_PASSANT"))
        abilities.append(MovementAbility(max_units=1, direction=(-1, -1), circumstance="EN_PASSANT"))
        return abilities


if __name__ == '__main__':
    a_one = Square(file=File.A, rank=Rank.ONE, colour=Colour.WHITE)
    a_one_colour = square_colour(a_one.rank, a_one.file)

    squares = create_all_squares()

    the_mighty_king = King(colour=Colour.WHITE)
    yas_queen = Queen(colour=Colour.BLACK)
    a_rook = Rook(colour=Colour.WHITE)
    a_bishop = Bishop(colour=Colour.WHITE)
    a_knight = Knight(colour=Colour.WHITE)
    a_white_pawn = WhitePawn()
    a_black_pawn = BlackPawn()

    print('The mighty King\'s moves are: ')
    for move in the_mighty_king.move_abilities():
        print(move)

    print('\n Yas Queen\'s moves are: ')
    for move in yas_queen.move_abilities():
        print(move)

    print('\n A rook\'s moves are: ')
    for move in a_rook.move_abilities():
        print(move)

    print('\n A bishop\'s moves are: ')
    for move in a_bishop.move_abilities():
        print(move)

    print('\n A knight\'s moves are: ')
    for move in a_knight.move_abilities():
        print(move)

    print('\n A white pawn\'s moves are: ')
    for move in a_white_pawn.move_abilities():
        print(move)

    print('\n A black pawn\'s moves are: ')
    for move in a_black_pawn.move_abilities():
        print(move)

    print('stop here')
