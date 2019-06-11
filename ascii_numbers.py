"""
This program takes an input string, and prints it out in a banner
format.
"""

# Height of our characters
line_height = 7

# List of characters
letters = []

letter = """
 ### 
#   #
#   #
#   #
#   #
#   #
 ### 
"""
letters.append(letter.split("\n"))

letter = """
 # 
## 
 # 
 # 
 # 
 # 
###
"""
letters.append(letter.split("\n"))

letter = """
 ### 
#   #
    #
   # 
  #  
 #   
#####
"""
letters.append(letter.split("\n"))

letter = """
 ### 
#   #
    #
  ## 
    #
#   #
 ### 
"""
letters.append(letter.split("\n"))

letter = """
#   # 
#   # 
#   # 
######
    # 
    # 
    # 
"""
letters.append(letter.split("\n"))

letter = """
#####
#    
#    
#### 
    #
    #
#### 
"""
letters.append(letter.split("\n"))

letter = """
 ### 
#   #
#    
#### 
#   #
#   #
 ### 
"""
letters.append(letter.split("\n"))

letter = """
#####
    #
    #
   # 
  #  
 #   
#    
"""
letters.append(letter.split("\n"))

letter = """
 ### 
#   #
#   #
 ### 
#   #
#   #
 ### 
"""
letters.append(letter.split("\n"))

letter = """
 ### 
#   #
#   #
#####
    #
#   #
 ### 
"""
letters.append(letter.split("\n"))

letter = """
  
  
  
  
  
##
##
"""
letters.append(letter.split("\n"))

# Create a mapping of character letters, to letters in our list
mapping_characters = "0123456789."
mapping_indexes = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10


def print_string(input_string: str):
    """
    Print out the string in a banner format.

    :param input_string: Input string
    """

    # Create a list that, instead of the string, has the index locations
    # of our banner characters. So instead of "1.2" we have [1, 10, 2]
    index_locations = []
    for character in input_string:
        if character in mapping_characters:
            my_index = mapping_characters.index(character)
            index_locations.append(my_index)

    # Now loop through each line
    for line_no in range(1, line_height + 1):
        # Loop though each index location to print
        for character in index_locations:
            # Print that line of the character
            print(letters[character][line_no], end="  ")
        # Go to the next line
        print()

print_string("3.141592653")
print()
print_string("1.41421")