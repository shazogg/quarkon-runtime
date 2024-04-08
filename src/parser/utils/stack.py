# Is stack empty
def is_empty(stack):
    return len(stack) == 0

# Push item to stack
def push(stack, item):
    stack.append(item)

# Pop item from stack
def pop(stack):
    if is_empty(stack):
        return None
    return stack.pop()

# Get top item from stack
def top(stack):
    if is_empty(stack):
        return None
    return stack[-1]

# Get size of stack
def size(stack):
    return len(stack)