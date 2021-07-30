from abc import ABC, abstractmethod
import pydantic
from pydantic import BaseModel
from enum import Enum
from typing import List, Tuple, Optional, Dict
import math

from termcolor import colored
from colorama import init, Fore, Back, Style


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


class Board:
    def __init__(self, opening_pos:bool):
        self.captured_pieces: List[Piece] = []
        self.shape = 64
        self.configuration: Dict[Square, Piece] = {}
        self.squares: List[Square] = []
        self.create_all_squares()

        if opening_pos is True:
            self.set_opening_position()

    def create_all_squares(self) -> List[Square]:  # Todo I want to be able to refer to an individual square, not an index of this list
        self.squares = [
            Square(file=file, rank=rank, colour=square_colour(rank, file))
            for rank in Rank for file in File
        ]
        return self.squares

    def set_opening_position(self):
        _board = {  # Todo here I am recreating the squares?
            Square(rank=Rank.ONE, file=File.A, colour=Colour.BLACK): Rook(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.B, colour=Colour.WHITE): Knight(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.C, colour=Colour.BLACK): Bishop(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.D, colour=Colour.WHITE): Queen(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.E, colour=Colour.BLACK): King(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.F, colour=Colour.WHITE): Bishop(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.G, colour=Colour.BLACK): Knight(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.H, colour=Colour.WHITE): Rook(colour=Colour.WHITE),
            Square(rank=Rank.TWO, file=File.A, colour=Colour.BLACK): WhitePawn,
            Square(rank=Rank.TWO, file=File.B, colour=Colour.WHITE): WhitePawn,
            Square(rank=Rank.TWO, file=File.C, colour=Colour.BLACK): WhitePawn,
            Square(rank=Rank.TWO, file=File.D, colour=Colour.WHITE): WhitePawn,
            Square(rank=Rank.TWO, file=File.E, colour=Colour.BLACK): WhitePawn,
            Square(rank=Rank.TWO, file=File.F, colour=Colour.WHITE): WhitePawn,
            Square(rank=Rank.TWO, file=File.G, colour=Colour.BLACK): WhitePawn,
            Square(rank=Rank.TWO, file=File.H, colour=Colour.WHITE): WhitePawn,
            Square(rank=Rank.EIGHT, file=File.A, colour=Colour.BLACK): Rook(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.B, colour=Colour.WHITE): Knight(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.C, colour=Colour.BLACK): Bishop(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.D, colour=Colour.WHITE): Queen(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.E, colour=Colour.BLACK): King(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.F, colour=Colour.WHITE): Bishop(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.G, colour=Colour.BLACK): Knight(colour=Colour.WHITE),
            Square(rank=Rank.ONE, file=File.H, colour=Colour.WHITE): Rook(colour=Colour.WHITE),
            Square(rank=Rank.TWO, file=File.A, colour=Colour.BLACK): WhitePawn,
            Square(rank=Rank.TWO, file=File.B, colour=Colour.WHITE): WhitePawn,
            Square(rank=Rank.TWO, file=File.C, colour=Colour.BLACK): WhitePawn,
            Square(rank=Rank.TWO, file=File.D, colour=Colour.WHITE): WhitePawn,
            Square(rank=Rank.TWO, file=File.E, colour=Colour.BLACK): WhitePawn,
            Square(rank=Rank.TWO, file=File.F, colour=Colour.WHITE): WhitePawn,
            Square(rank=Rank.TWO, file=File.G, colour=Colour.BLACK): WhitePawn,
            Square(rank=Rank.TWO, file=File.H, colour=Colour.WHITE): WhitePawn,
                  }
        return self.configuration


def square_colour(rank: Rank, file: File) -> Colour:
    file_num = list(File).index(file) + 1
    rank_num = rank.value
    #  chessboard squares are black if rank and file are both odd, or both even.
    return Colour.BLACK if (file_num % 2 == rank_num % 2) else Colour.WHITE


def display_board1(squares):
    rank_counter = 56
    termcolor_dict = {'White': 'on_white', 'Black':'on_red'}
    for rank in range(9, 1, -1):
        for file in range(0, 8, 1):
            square_colour = squares[rank_counter+file].colour.value
            print(colored(squares[rank_counter+file].file.value, on_color=termcolor_dict[square_colour]), end="")
            print(colored(squares[rank_counter+file].rank.value, on_color=termcolor_dict[square_colour]), end="   ")
        print('\n')
        rank_counter -= 8


def display_board2(squares):
    init(autoreset=True)
    rank_counter = 56
    for rank in range(9, 1, -1):
        for file in range(0, 8, 1):
            if squares[rank_counter+file].colour.value == 'Black':
                print(Style.BRIGHT + Back.BLACK + Fore.WHITE+ f'{squares[rank_counter+file].file.value}', end="")
                print(Style.BRIGHT + Back.BLACK + Fore.WHITE + f'{squares[rank_counter+file].rank.value}', end="   ")
            else:
                print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f'{squares[rank_counter+file].file.value}', end="")
                print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f'{squares[rank_counter+file].rank.value}', end="   ")
        print('\n')
        rank_counter -= 8


def initialise_starting_position():
    pass


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

    board = Board()
    squares = board.create_all_squares()
    display_board2(squares)

    the_mighty_king = King(colour=Colour.WHITE)
    yas_queen = Queen(colour=Colour.BLACK)
    a_rook = Rook(colour=Colour.WHITE)
    a_bishop = Bishop(colour=Colour.WHITE)
    a_knight = Knight(colour=Colour.WHITE)
    a_white_pawn = WhitePawn()
    a_black_pawn = BlackPawn()

    # print('The mighty King\'s moves are: ')
    # for move in the_mighty_king.move_abilities():
    #     print(move)
    #
    # print('\n Yas Queen\'s moves are: ')
    # for move in yas_queen.move_abilities():
    #     print(move)
    #
    # print('\n A rook\'s moves are: ')
    # for move in a_rook.move_abilities():
    #     print(move)
    #
    # print('\n A bishop\'s moves are: ')
    # for move in a_bishop.move_abilities():
    #     print(move)
    #
    # print('\n A knight\'s moves are: ')
    # for move in a_knight.move_abilities():
    #     print(move)
    #
    # print('\n A white pawn\'s moves are: ')
    # for move in a_white_pawn.move_abilities():
    #     print(move)
    #
    # print('\n A black pawn\'s moves are: ')
    # for move in a_black_pawn.move_abilities():
    #     print(move)

    print('stop here')
