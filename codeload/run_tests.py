import subprocess
import re


class App:
    def __init__(self, source_name):
        self.name = source_name
        self.built = False
        self.output_name = None

    def build(self, output_name = 'a'):
        self.output_name = output_name
        self.built = not bool(subprocess.run(['g++', self.name, '-o', output_name]).returncode)
        # print(f'self.built = {self.built}')
        return self.built

    def run(self, input):
        if (self.built):
            run = subprocess.run(
                './{}'.format(self.output_name),
                input=str(input),
                encoding='ascii',
                stdout=subprocess.PIPE 
            )
            return run.stdout
        raise IOError("Looks like application is not built")        

    def test(self, input, output):
            out = self.run(input)
            return self.run(input) == str(output.strip())

    def __repr__(self):
        with open(self.name) as source:
            return ''.join([i for i in source])


class Unit_Test:
    def __init__(self, source_name, tests_name):
        self.app = App(source_name)
        self.app.build()
        self.error_line = None
        # Test line should be like 'input, output'
        # e.g. '123 123, 246' 
        self.tname = tests_name

    def run_tests(self):
        with open(self.tname, 'r') as t:
            row = 0
            for i in t:
                if (not self.app.test(*i.split(','))):
                    self.error_line = row
                    return (False, row)
                row += 1
            return (True, -1)

    def get_error_line(self):
        return self.error_line

    def set_test_name(self, name):
        self.tname = name
    

if __name__ == '__main__':
    app = Unit_Test('../uploads/1.cpp', '../solution_tests/1.txt')
    print(app.run_tests())
