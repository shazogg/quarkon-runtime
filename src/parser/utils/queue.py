# Is queue empty
def is_empty(queue):
    return len(queue) == 0

# Push item to queue
def push(queue, item):
    queue.append(item)

# Push item to the front of the queue
def push_front(queue, item):
    queue.insert(0, item)

# Pop item from queue
def pop(queue):
    if is_empty(queue):
        return None
    return queue.pop(0)

# Push item to the back of the queue
def pop_back(queue):
    if is_empty(queue):
        return None
    return queue.pop()

# Get top item from queue
def top(queue):
    if is_empty(queue):
        return None
    return queue[0]

# Get back item from queue
def back(queue):
    if is_empty(queue):
        return None
    return queue[-1]

# Get size of queue
def size(queue):
    return len(queue)