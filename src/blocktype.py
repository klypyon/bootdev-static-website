from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    """
    Converts a block string to its corresponding BlockType enum value.
    Raises ValueError if the block string does not match any BlockType.
    """
    if re.match(r"#{1,6}\s", block):
        return BlockType.HEADING
    if re.match(r"```(\n).*?```", block, re.DOTALL):
        return BlockType.CODE

    lines = block.split("\n")
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("-") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH