import pprint
pp = pprint.PrettyPrinter(indent=2)
def get_input_for(name: str) -> str:
    pp.pprint(name + '\n')
    r = input('input is ' + name)
    return r.strip()