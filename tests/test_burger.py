import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


class TestBurger:
    def test_set_buns(self):
        burger = Burger()
        bun_mock = Mock()
        burger.set_buns(bun_mock)
        assert burger.bun == bun_mock

    def test_add_ingredient(self):
        burger = Burger()
        ingredient_mock = Mock()
        burger.add_ingredient(ingredient_mock)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ingredient_mock

    @pytest.mark.parametrize(
        "index,initial_ids,expected_ids",
        [
            (0, [1, 2, 3], [2, 3]),
            (1, [1, 2, 3], [1, 3]),
            (2, [1, 2, 3], [1, 2]),
        ],
    )
    def test_remove_ingredient(self, index, initial_ids, expected_ids):
        burger = Burger()
        mocks = [Mock() for _ in initial_ids]
        burger.ingredients = mocks
        burger.remove_ingredient(index)
        expected = [mocks[i - 1] for i in expected_ids]  # ids начинаются с 1
        assert burger.ingredients == expected

    @pytest.mark.parametrize(
        "index,new_index,initial_ids,expected_ids",
        [
            (0, 2, [1, 2, 3], [2, 3, 1]),
            (1, 0, [1, 2, 3], [2, 1, 3]),
            (2, 1, [1, 2, 3], [1, 3, 2]),
        ],
    )
    def test_move_ingredient(self, index, new_index, initial_ids, expected_ids):
        burger = Burger()
        mocks = [Mock() for _ in initial_ids]
        burger.ingredients = mocks
        burger.move_ingredient(index, new_index)
        expected = [mocks[i - 1] for i in expected_ids]
        assert burger.ingredients == expected

    def test_get_price(self):
        burger = Burger()
        bun_mock = Mock()
        bun_mock.get_price.return_value = 100
        burger.set_buns(bun_mock)

        ing1 = Mock()
        ing1.get_price.return_value = 50
        ing2 = Mock()
        ing2.get_price.return_value = 30
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)

        assert burger.get_price() == 100 * 2 + 50 + 30

    def test_get_price_no_ingredients(self):
        burger = Burger()
        bun_mock = Mock()
        bun_mock.get_price.return_value = 150
        burger.set_buns(bun_mock)
        assert burger.get_price() == 300

    def test_get_receipt(self):
        burger = Burger()
        bun_mock = Mock()
        bun_mock.get_name.return_value = "black bun"
        bun_mock.get_price.return_value = 100
        burger.set_buns(bun_mock)

        ing1 = Mock()
        ing1.get_type.return_value = "SAUCE"
        ing1.get_name.return_value = "hot sauce"
        ing1.get_price.return_value = 50
        burger.add_ingredient(ing1)

        ing2 = Mock()
        ing2.get_type.return_value = "FILLING"
        ing2.get_name.return_value = "cutlet"
        ing2.get_price.return_value = 70
        burger.add_ingredient(ing2)

        expected = """(==== black bun ====)
= sauce hot sauce =
= filling cutlet =
(==== black bun ====)

Price: 320"""
        assert burger.get_receipt() == expected

    def test_get_receipt_no_ingredients(self):
        burger = Burger()
        bun_mock = Mock()
        bun_mock.get_name.return_value = "white bun"
        bun_mock.get_price.return_value = 200
        burger.set_buns(bun_mock)

        expected = """(==== white bun ====)
(==== white bun ====)

Price: 400"""
        assert burger.get_receipt() == expected