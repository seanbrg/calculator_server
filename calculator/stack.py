from calculator.operations import OPERATIONS

class StackManager:
    def __init__(self):
        self.stack = []

    def push(self, values):
        """Push a list of values onto the stack."""
        if not all(isinstance(v, int) for v in values):
            raise ValueError("All arguments must be integers")
        self.stack.extend(values)

    def pop(self, count):
        """Pop `count` items from the top of the stack."""
        if count > len(self.stack):
            raise ValueError(
                f"Error: cannot remove {count} from the stack. It has only {len(self.stack)} arguments"
            )
        for _ in range(count):
            self.stack.pop()

    def size(self):
        """Return current stack size."""
        return len(self.stack)

    def peek(self, op_name):
        """
        Check if there are enough arguments for the given operation.
        Return the required number of arguments without removing them.
        Raise ValueError if not enough.
        """
        op_name = op_name.lower()
        if op_name not in OPERATIONS:
            raise ValueError(f"Error: unknown operation: {op_name}")

        _, required = OPERATIONS[op_name]

        if len(self.stack) < required:
            raise ValueError(
                f"Error: cannot implement operation {op_name}. It requires {required} arguments and the stack has only {len(self.stack)} arguments"
            )

        # Top of stack is the end of the list
        return self.stack[-required:][::-1]  # Return in LIFO order: top is first
