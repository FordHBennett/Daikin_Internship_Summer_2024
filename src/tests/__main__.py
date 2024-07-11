import unittest

class CustomTextTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_class_hierarchy = []


    def startTest(self, test):
        test_class = test.__class__
        class_hierarchy = self._get_class_hierarchy(test_class)
        self._print_class_hierarchy(class_hierarchy)
        super().startTest(test)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln(f"\033[92m\t{self.indent}SUCCESS: {test}\033[0m")
        self.stream.writeln("\n")

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.writeln(f"\033[91m\tERROR: {test}\033[0m")
        self.stream.writeln(f"\t{err}")
        self.stream.writeln("\n")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.writeln(f"\033[91m\tFAILURE: {test}\033[0m")
        self.stream.writeln(f"\t{err}")
        self.stream.writeln("\n")

    def _get_class_hierarchy(self, cls):
        cls = (cls.__module__.split('.'))[1:]
        return cls


    def _print_class_hierarchy(self, class_hierarchy):
        for i, cls in enumerate(class_hierarchy):
            if i >= len(self.current_class_hierarchy) or self.current_class_hierarchy[i] != cls:
                self.current_class_hierarchy = class_hierarchy[:i+1]
                self.indent = '\t' * i
                self.stream.writeln(f"\n{self.indent}{cls}\n{self.indent}{'=' * len(cls)}")



class CustomTextTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    runner = CustomTextTestRunner(verbosity=1)
    runner.run(suite)