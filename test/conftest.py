from pytest import fixture


@fixture
def stdout(capsys):
    def func():
        out, _ = capsys.readouterr()
        return out
    return func
