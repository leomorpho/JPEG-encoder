from typing import List
import math
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def zigzag(block: List[List[int]]):
    """
    Zigzag over a block to create a vector. Encode using Huffman encoding.
    """
    log.info("Zigzagging block into vector")

    vector = []

    max_index = len(block) - 1

    # Current location of cursor
    x, y = 0, 0

    vector.append(block[y][x])
    log.debug(f"{x}, {y}")

    while True:
        # Go one step right or down
        if x < max_index:
            x += 1
        elif y < max_index:
            y += 1
        else:
            break

        vector.append(block[y][x])
        log.debug(f"{x}, {y}")

        # Traverse diagonal towards bottom-left
        while True:
            y += 1
            x -= 1
            if y > max_index or x < 0:
                # Arrived at right or bottom edge of block
                y -= 1
                x += 1
                break
            vector.append(block[y][x])
            log.debug(f"{x}, {y}")

        # Go one step down or right
        if y < max_index:
            y += 1
        elif x < max_index:
            x += 1
        else:
            break

        vector.append(block[y][x])
        log.debug(f"{x}, {y}")

        # Traverse diagonal towards top-right
        while True:
            y -= 1
            x += 1
            if y < 0 or x > max_index:
                # Arrived at top or left edge of block
                y += 1
                x -= 1
                break
            vector.append(block[y][x])
            log.debug(f"{x}, {y}")

    return vector

def un_zigzag(vector: [List[int]]):
    """
    Decode using Huffman decoding. Create a block from the decoded vector.
    """
    log.info("Unzigzagging vector into block")

    edge_val_count = int(math.sqrt(len(vector)))
    max_index = edge_val_count - 1

    # Create zero matrix of required size
    block = [[0 for i in range(edge_val_count)] for i in range(edge_val_count)]

    # Current location of cursor
    x, y = 0, 0

    block[y][x] = vector.pop(0)
    log.debug(f"{x}, {y}")

    while True:
        # Go one step right or down
        if x < max_index:
            x += 1
        elif y < max_index:
            y += 1
        else:
            break

        block[y][x] = vector.pop(0)
        log.debug(f"{x}, {y}")

        # Traverse diagonal towards bottom-left
        while True:
            y += 1
            x -= 1
            if y > max_index or x < 0:
                # Arrived at right or bottom edge of block
                y -= 1
                x += 1
                break
            block[y][x] = vector.pop(0)
            log.debug(f"{x}, {y}")

        # Go one step down or right
        if y < max_index:
            y += 1
        elif x < max_index:
            x += 1
        else:
            break

        block[y][x] = vector.pop(0)
        log.debug(f"{x}, {y}")

        # Traverse diagonal towards top-right
        while True:
            y -= 1
            x += 1
            if y < 0 or x > max_index:
                # Arrived at top or left edge of block
                y += 1
                x -= 1
                break
            block[y][x] = vector.pop(0)
            log.debug(f"{x}, {y}")

    return block
