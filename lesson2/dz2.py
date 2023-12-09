from random import randint
import numpy as np
import random


class Keg:
    def __init__(self, first_keg, last_keg):
        self.first_keg = first_keg
        self.last_keg = last_keg

    def get_random_keg(self):
        return randint(self.first_keg, self.last_keg)


class KegBag(Keg):
    def __init__(self, first_keg, last_keg):
        super().__init__(first_keg, last_keg)
        self.kegs_in_bag = list(range(self.first_keg, self.last_keg + 1))

    def delete_keg_from_bag(self, current_keg):
        self.kegs_in_bag.remove(current_keg)

    def get_remaining_kegs_in_bag(self):
        # print(f'Remaining kegs in_bag: {self.kegs_in_bag}')
        return self.kegs_in_bag

    def get_random_keg_from_bag(self):
        return random.choices(self.kegs_in_bag)[0]


class Card(Keg):
    def __init__(self, first_keg, last_keg, card_rows, items_in_row, nums_in_row):
        super().__init__(first_keg, last_keg)
        self.card_rows = card_rows
        self.items_in_row = items_in_row
        self.nums_in_row = nums_in_row
        self.empty_items = self.items_in_row - self.nums_in_row

    @property
    def card_rows(self):
        return self._card_rows

    @card_rows.setter
    def card_rows(self, value):
        if type(value) is not int:
            raise TypeError("Count of rows is not int")
        if value not in (3, 4, 5):
            raise ValueError("Invalid value")
        self._card_rows = value

    @property
    def items_in_row(self):
        return self._items_in_row

    @items_in_row.setter
    def items_in_row(self, value):
        if type(value) is not int:
            raise TypeError("Count of items is not int")
        if value not in (8, 9, 10):
            raise ValueError("Invalid value")
        self._items_in_row = value

    @property
    def nums_in_row(self):
        return self._nums_in_row

    @nums_in_row.setter
    def nums_in_row(self, value):
        if type(value) is not int:
            raise TypeError("Count of nums type is not int")
        if value not in (4, 5, 6):
            raise ValueError("Invalid value")
        self._nums_in_row = value

    def generate_card_values(self) -> list:
        nums_list = []
        while len(nums_list) < self.card_rows * self.nums_in_row:
            random_num_for_card = Keg(self.first_keg, self.last_keg).get_random_keg()
            if random_num_for_card not in nums_list:
                nums_list.append(random_num_for_card)

        card_values_list = []
        chunked_array = np.array_split(nums_list, self.card_rows)
        for arr in chunked_array:
            card_row = [0] * self.empty_items + list(arr)
            random.shuffle(card_row)
            card_values_list += card_row
        card_values_list = list(map(str, card_values_list))
        # print(f'Card values: {card_values_list}')
        return card_values_list

    def generate_visual_card(self, card_values_list) -> str:
        visual_card_values = []
        for count, value in enumerate(card_values_list, 1):
            if value == '0':
                value = '  '
            if len(value) == 1:
                value = f'{value} '
            if count.__mod__(self.items_in_row) == 0:
                value = f'{value}\n'
            visual_card_values.append(value)
        card_title = '-------------------------------\n '
        visual_card = card_title + ' '.join(visual_card_values) + card_title
        # print(visual_card)
        return visual_card

    @staticmethod
    def cross_out_card_value(num, values_list) -> list:
        return ['--' if value == str(num) else value for value in values_list]

    def checking_card_closing(self, card_values, gamer) -> bool:
        checking_card = card_values.count('--') == self.card_rows * self.nums_in_row
        if checking_card:
            print(f'{gamer} card was closed, finish Game!')
        return checking_card


class Player:
    def __init__(self, first_keg, last_keg, card_rows, items_in_row, nums_in_row, gamer):
        self.card = Card(first_keg, last_keg, card_rows, items_in_row, nums_in_row)
        self.player_card_values = self.card.generate_card_values()
        self.gamer = gamer

    def visual_card(self):
        return self.card.generate_visual_card(self.player_card_values)

    def update_player_card(self, current_keg, player_answer):
        if self.card.checking_card_closing(self.player_card_values, self.gamer):
            return False
        for num in self.player_card_values:
            if str(current_keg) == num:
                if player_answer == 'y':
                    print(f'\n{self.gamer} cross out card value\n')
                    self.player_card_values = self.card.cross_out_card_value(current_keg, self.player_card_values)
                    self.visual_card()
                    return True
                else:
                    print(f'\n{self.gamer} lose, num of current keg was in card!\n')
                    return False
        if player_answer == 'y':
            print(f'\n{self.gamer} lose, num of current keg not in card!\n')
            return False
        return True


class Computer:
    def __init__(self, first_keg, last_keg, card_rows, items_in_row, nums_in_row, gamer):
        self.card = Card(first_keg, last_keg, card_rows, items_in_row, nums_in_row)
        self.computer_card_values = self.card.generate_card_values()
        self.gamer = gamer

    def visual_card(self):
        return self.card.generate_visual_card(self.computer_card_values)

    def update_computer_card(self, current_keg):
        if self.card.checking_card_closing(self.computer_card_values, self.gamer):
            return False
        else:
            for num in self.computer_card_values:
                if str(current_keg) == num:
                    print(f'\n{self.gamer} cross out card value\n')
                    self.computer_card_values = self.card.cross_out_card_value(current_keg, self.computer_card_values)
                    self.card.generate_visual_card(self.computer_card_values)
            return True


class Game(Keg):
    def __init__(self, first_keg, last_keg, card_rows, items_in_row, nums_in_row, mode):
        super().__init__(first_keg, last_keg)
        self.keg_bag = KegBag(first_keg, last_keg)
        self.mode = mode
        if self.mode == 'player and computer':
            self.player = Player(first_keg, last_keg, card_rows, items_in_row, nums_in_row, 'Player')
            self.computer = Computer(first_keg, last_keg, card_rows, items_in_row, nums_in_row, 'Computer')
        if self.mode == '2 computers':
            self.computer_1 = Computer(first_keg, last_keg, card_rows, items_in_row, nums_in_row, 'Computer 1')
            self.computer_2 = Computer(first_keg, last_keg, card_rows, items_in_row, nums_in_row, 'Computer 2')
        if self.mode == '2 players':
            self.player_1 = Player(first_keg, last_keg, card_rows, items_in_row, nums_in_row, 'Player 1')
            self.player_2 = Player(first_keg, last_keg, card_rows, items_in_row, nums_in_row, 'Player 2')

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if type(value) is not str:
            raise TypeError("Mode type is not string")
        if value not in ('player and computer', '2 players', '2 computers'):
            raise ValueError("Non-existent game mod")
        self._mode = value

    def make_move(self):
        current_keg = self.keg_bag.get_random_keg_from_bag()
        self.keg_bag.delete_keg_from_bag(current_keg)
        remaining_kegs = self.keg_bag.get_remaining_kegs_in_bag()
        print(f'Новый бочонок:{current_keg} (осталось {len(remaining_kegs)})\n')

        if self.mode == 'player and computer':
            print(f'------ Карточка игрока --------\n{self.player.visual_card()}')
            print(f'----- Карточка компьютера -----\n{self.computer.visual_card()}')
            player_answer = input(f'Зачеркнуть цифру {current_keg}? (y/n)')
            return self.computer.update_computer_card(current_keg) and \
                self.player.update_player_card(current_keg, player_answer) is True

        if self.mode == '2 computers':
            print(f'------ Карточка компьютера 1 --------\n{self.computer_1.visual_card()}')
            print(f'------ Карточка компьютера 2 --------\n{self.computer_2.visual_card()}')
            self.computer_1.update_computer_card(current_keg)
            self.computer_2.update_computer_card(current_keg)
            return self.computer_1.update_computer_card(current_keg) and \
                self.computer_2.update_computer_card(current_keg) is True

        if self.mode == '2 players':
            print(f'------ Карточка игрока 1--------\n{self.player_1.visual_card()}')
            print(f'------ Карточка игрока 2 -------\n{self.player_2.visual_card()}')
            player_1_answer = input(f'Игрок 1, зачеркнуть цифру {current_keg}? (y/n)')
            player_2_answer = input(f'Игрок 2, зачеркнуть цифру {current_keg}? (y/n)')
            return self.player_1.update_player_card(current_keg, player_1_answer) and \
                self.player_2.update_player_card(current_keg, player_2_answer) is True

    def play(self):
        for _ in range(self.last_keg):
            if not self.make_move():
                break


if __name__ == '__main__':
    game = Game(1, 90, 3, 9, 5, mode='player and computer')
    game.play()
