from calculator import is_number
import calculator as cl
import pytest

#UNIT TEST
#Test Calculator
@pytest.mark.parametrize("expression, expected", [
    ("2+3", "5.0"),
    ("2*3", "6.0"),
    ("10/2", "5.0"),
    ("-13.3+(-31.2)*0.1",str(-13.3 + (-31.2) * 0.1))
])
def test_calculator(expression, expected):
    result = cl.Calculator(expression)
    assert result.answer == expected

#тест статик функций
@pytest.mark.parametrize("expression, expected",[
    ("5",True),
    ("0",True),
    ("abc",False)
])
def test_is_number_number(expression,expected):
    assert is_number(expression) == expected

#Токенизатор
def test_tokenizer():
    result = cl.Tokenizer("2+3")
    result.run()
    assert result.data_tokenizer == ["2","+","3"]

def test_tokenizer_error2():
    t = cl.Tokenizer("2++3")
    with pytest.raises(cl.TokenizerError):
        t.run()

def test_tokenizer_bad_input():
    result = cl.Calculator("2--3")
    assert result.answer == ""

def test_tokenizer_float_error():
    t = cl.Tokenizer("(13..)")
    with pytest.raises(cl.TokenizerError):
        t.run()


# RPN
def test_rpn_unary_minus():
    result = cl.RPN(['-', '2', '+', '3', '+', '4'])
    result.run()
    assert result.queue == ['2', '~', '3', '+', '4', '+']

def test_rpn_bracket():
    result = cl.RPN(['(', '-', '2', '+', '3', '+', '4', ')'])
    result.run()
    assert result.queue == ['2', '~', '3', '+', '4', '+']
# Count
def test_count_devine_0():
    t = cl.Count(["10","0","/"])
    with pytest.raises(cl.CountError):
        t.run()

def test_count_unary_minus():
    result = cl.Count(["2","~"])
    result.run()
    assert result.stack == ["-2"]

def test_count_op():
    result = cl.Count(["2","~"])
    result.run()
    assert result.stack == ["-2"]

@pytest.mark.parametrize("expression, expected", [
    ("*2", ""),
    ("/2", ""),
    ("-2", "-2"),
    ("+2","")
])
def test_count_op_under(expression, expected):
    result = cl.Calculator(expression)
    assert result.answer == expected

@pytest.mark.parametrize("expression, expected", [
    (['3', '2', '*'], ['6.0']),
    (['4', '2', '/'], ['2.0']),
    (['5', '2', '-'], ['3.0']),
    (['6', '2', '+'], ['8.0'])
])
def test_count_op_after(expression, expected):
    result = cl.Count(expression)
    result.run()
    assert result.stack == expected
