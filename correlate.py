from collections import defaultdict, namedtuple
from jpprint import jpprint

data = defaultdict(lambda: defaultdict(list))
img_line = namedtuple('ImgLine', ['id', 'company', 'pol_number', 'gen_time'])

def write_lines(file_name):
    with open(file_name, 'w') as f:
        while True:
            line = yield
            if line is None:
                break
            f.write(line)

def close_corout(corout):
    try:
        corout.send(None)
    except StopIteration:
        print('Closed', corout.__name__)

def create_namedtuple(line, tup):
    l = line.split('|')
    if len(l) != 5 or not l[1].strip().isdigit():
        continue
    return tup(*[x for i, x in enumerate(l) if x and i in [0, 1, 2, 3, 4]])

with open('test.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    l = create_namedtuple(line, img_line)
    data[l.company.strip()][l.pol_number.strip()].append({'id': l.id.strip(), 'time': l.gen_time.strip()})

with open('test_comp.txt', 'r') as f:
    comp_lines = f.readlines()

success = write_lines('success.txt')
failure = write_lines('failure.txt')
next(success)
next(failure)

# TODO compare lines from one to the data structure
vec_line = namedtuple('VecLine', ['id', 'company', 'policy', 'name'])
with open('test_comp.txt', 'r') as f:
    comp_lines = f.readlines()


for line in comp_lines:
    li = create_namedtupe(line, vec_line)
    var = data.get(li.company).get(li.policy)
    for value in var:
        if value['time'].replace(':', '')[:14] == li.name[:14]:
            success.send('{} | {}\n'.format(li.name, li.policy))
        else:
            failure.send('{} | {}\n'.format(li.name, li.policy))

close_corout(success)
close_corout(failure)
