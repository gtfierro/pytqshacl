from pathlib import Path

def get_pth(fn):
    _ = Path(__file__).parent
    _ = _ / fn
    assert(_.exists())
    return _
data =      get_pth('data.ttl')
shapes =    get_pth('shapes.ttl')

def test_infer():
    from pytqshacl import infer
    _ = infer(data, shapes=shapes)
    assert('99' in _.stdout)

def test_validate():
    from pytqshacl import validate
    _ = validate(data, shapes=shapes)
    assert('ValidationReport' in _.stdout)

def all():
    print('testing inference')
    test_infer()
    print('testing validation')
    test_validate()
    print('np')

if __name__ == '__main__':
    all()
    