# Compare two lists. Return True if a[i] >= b[i] for all i
def compare(list_a, list_b, comparator=None):
    if len(list_a) != len(list_b):
        raise ValueError("Lists must have the same length")
    elif comparator is None:
        raise ValueError("Comparator must be specified")
    elif comparator not in ['>', '<', '>=', '<=', '==', '!=']:
        raise ValueError("Comparator must be one of '>', '<', '>=', '<=', '==', '!='")
    else:
        for i in range(len(list_a)):
            if not eval( str(list_a[i]) + comparator + str(list_b[i]) ):
                return False
        return True

# Add/subtract two lists
def merge(list_a, list_b, direction=None):
    if len(list_a) != len(list_b):
        raise ValueError("Lists must have the same length")
    if direction is None:
        raise ValueError("direction must be specified")
    elif direction not in ['+', '-']:
        raise ValueError("direction must be one of '+', '-'")
    return [
            eval(str(list_a[i]) + direction + str(list_b[i])) for i in range(len(list_a))
        ]