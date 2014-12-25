import unittest
import sys
import os
import time
class GameOfLifeTest(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_cell_has_position(self):
        cell = Cell((0,0), 'live')
        self.assertEqual(cell.position,(0,0))

    def test_live_cell_list_should_contain_live_cells_position(self):
        cell1 = Cell((0, 0), 'live')
        cell2 = Cell((1, 0), 'live')
        cell3 = Cell((1, 1), 'live')
        self.board.first_gen_list = [cell1, cell2]
        self.assertEqual(self.board.first_gen_list, [cell1, cell2])

    def test_live_cell_with_less_than_two_neighbors_should_return_die(self):
        status = self.board.check_status('live', 1)
        self.assertEqual(status, 'dead')

    def test_live_cell_with_2_or_3_neighbors_should_return_live(self):
        status = self.board.check_status('live', 2)
        self.assertEqual(status, 'live')

        status = self.board.check_status('live', 3)
        self.assertEqual(status, 'live')

    def test_live_cell_more_than_3_neighbors_should_return_die(self):
        status = self.board.check_status('live', 5)
        self.assertEqual(status, 'dead')

    def test_dead_cell_with_3_neighbors_should_return_die(self):
        status = self.board.check_status('dead', 3)
        self.assertEqual(status, 'live')

    def test_dead_cell_with_not_3_neighbors_should_return_die(self):
        status = self.board.check_status('dead', 4)
        self.assertEqual(status, 'dead')

    def test_find_live_neighbors(self):
        cell = Cell((0,0), 'live')
        self.board.first_gen_list = [cell , Cell((1,0), 'live'), Cell((1,1), 'live'), Cell((5,0), 'live')]
        result = self.board.find_neighbors(cell,self.board.first_gen_list)
        self.assertEqual(result,2)
     
    def test_find_live_neighbors(self):
        cell = Cell((0,0), 'live')
        self.board.first_gen_list = [cell , Cell((-1,1), 'live'), Cell((-1,0), 'live'), Cell((-1,-1), 'live'),
        Cell((0,1), 'live'), Cell((0,-1), 'live'), Cell((1,1), 'live'), Cell((1,0), 'live'), Cell((1,-1), 'live'), Cell((5,0), 'live')]
        result = self.board.find_neighbors(cell)
        self.assertEqual(result,8)

    def test_add_dead_cells_to_first_gen_list(self):
        cell = Cell((0,0), 'live')
        self.board.first_gen_list = [cell]
        result = self.board.add_dead_cell()
        expected = [cell, Cell((-1,1), 'dead'), Cell((-1,0), 'dead'), Cell((-1,-1), 'dead'),
            Cell((0,1), 'dead'), Cell((0,-1), 'dead'), Cell((1,1), 'dead'), Cell((1,0), 'dead'), Cell((1,-1), 'dead')]
        self.assertItemsEqual(self.board.first_gen_list,expected)

    def test_add_deads_cells_with_two_live_cells(self):
        cell1 = Cell((0,0), 'live')
        cell2 = Cell((0,1), 'live')
        self.board.first_gen_list = [cell1, cell2]
        expected =[cell1, cell2, Cell((1,-1), 'dead'), Cell((1,0), 'dead'), Cell((1,1), 'dead')
            , Cell((1,2), 'dead'), Cell((0,-1), 'dead'), Cell((0,2), 'dead') , Cell((-1,-1), 'dead')
            , Cell((-1,0), 'dead'), Cell((-1,1), 'dead'), Cell((-1,2), 'dead')]
        self.board.add_dead_cell()
        self.assertItemsEqual(self.board.first_gen_list,expected)
    
    def test_game_should_run_in_1_cycle(self):
        cell1 = Cell((0,0), 'live')
        cell2 = Cell((0,1), 'live')
        cell3 = Cell((1,2), 'live')
        cell4 = Cell((2,1), 'live')
        self.board.first_gen_list = [cell1, cell2, cell3, cell4]
        self.board.generation = 1
        self.board.run_game(unittest=True, generation=1)
        expected = [Cell((0,1),'live'), Cell((1, 2), 'live'), Cell((1, 0), 'live')]
        self.assertItemsEqual(self.board.first_gen_list,expected)

class Cell:
    def __init__(self, position, status):
        self.position = position
        self.status = status

    def __eq__(self, other):
        return (self.position == other.position and self.status == other.status)
    def __repr__(self):
        return "Cell(%s, %s)" % (self.position, self.status)
    def __hash__(self):
        return hash(self.__repr__())


def print_there(x, y, text):
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x+10, y+10, text))
    sys.stdout.flush()


class Board:
    def __init__(self):
        self.first_gen_list = []
    
    def print_first_gen_list(self):
        os.system('clear')
        for cell in self.first_gen_list:
            print_there(cell.position[0], cell.position[1], '*')
        time.sleep(1)

    def run_game(self, unittest=False, generation=1):
        second_gen_list = []
        while(generation > 0):
            if not unittest:
                self.print_first_gen_list()
            self.add_dead_cell()
            position_list = []
            for cell in self.first_gen_list:
                neighbors = self.find_neighbors(cell)
                status = self.check_status(cell.status, neighbors)
                if status == 'live':
                    if cell.status == 'dead':
                        cell = Cell(cell.position, 'live')
                    second_gen_list.append(cell)
            self.first_gen_list = list(second_gen_list)
            second_gen_list = []
            if type(generation) != bool:
                generation -= 1
            
    def add_dead_cell(self):
        first_gen_list = list(self.first_gen_list)
        position_list = []
        for each in first_gen_list:
            position_list.append(each.position)
         
        for cell in first_gen_list:
            for i in [-1, 0 , 1]:
                for j in [-1, 0, 1]:
                    posX = cell.position[0]+i
                    posY = cell.position[1]+j
                    position = (posX, posY)
                    if position not in position_list:
                        self.first_gen_list.append(Cell(position, 'dead'))
                        position_list.append(position)
                    
    def check_status(self, status, neighbors):
        result = ''
        if status == 'live':
            if neighbors < 2:
                result = 'dead'
            elif neighbors in [2, 3]:
                result = 'live'
            elif neighbors > 3:
                result = 'dead'
        else:
            if neighbors == 3:
                result = 'live'
            else:
                result = 'dead'
        return result

    def find_neighbors(self, cell):
        mycell_position = cell.position
        neighbors_list = []
        neighbors = 0
        for i in [-1, 0 , 1]:
            for j in [-1, 0, 1]:
                neighbors_list.append((mycell_position[0]+i, mycell_position[1]+j))
        neighbors_list.remove(mycell_position)
        for each in neighbors_list:
            for cell in self.first_gen_list:
                if each == cell.position and cell.status == 'live':
                    neighbors += 1
        return neighbors
                
import random                
if __name__ == '__main__':
    board = Board()
    os.system('clear')
    for i in range(30):
        x = random.randint(0,10)
        y = random.randint(0,10)
        cell = Cell((x,y), 'live')
        if cell not in board.first_gen_list:
            board.first_gen_list.append(cell)
    board.run_game(unittest=False, generation=True)
    #unittest.main()

