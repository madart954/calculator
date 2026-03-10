from calculator02 import is_number
import calculator02 as cl
import pytest

@pytest.mark.parametrize("expression, expected", [
    ("2+3", "5.0"),
    ("2*3", "6.0"),
    ("10/2", "5.0"),
    ("-13.3+(-31.2)*0.1",str(-13.3 + (-31.2) * 0.1))
])
def test_calculator(expression, expected):
    result = cl.Calculator(expression)
    assert result.answer == expected


@pytest.mark.parametrize("expression, expected",[
    ("5",True),
    ("0",True),
    ("abc",False)
])
#тест статик функций
def test_is_number_number(expression,expected):
    assert is_number(expression) == expected

def test_tokenizer():
    result = cl.Tokenizer("2+3")
    result.run()
    assert result.data_tokenizer == ["2","+","3"]

def test_tokenizer_error2():
    t = cl.Tokenizer("2++3")
    with pytest.raises(cl.TokenizerError):
        t.run()

def test_tokenizer_bad_input():
    rssult = cl.Calculator("2--3")
    assert rssult.answer == ""

