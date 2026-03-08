from calculator02 import is_number
import calculator02 as cl

#тест статик функций
def test_is_number_number():
    assert is_number("5")

def test_is_number_zero():
    assert is_number("0")

def test_is_number_abc():
    assert is_number("abc")  == False

def test_calculator_negative():
    result = cl.Calculator("-13.3+(-31.2)*0.1")
    assert result.answer == str(-13.3 + (-31.2) * 0.1)