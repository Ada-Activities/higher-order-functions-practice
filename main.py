# implement the following functions
# each must use the max() function in its implementation

WORDS = ["jumps", "laziest", "brown", "a", "quick", "fox", "the", "dog", "over"]

# find the word that is alphabetically "highest" (comes last alphabetically)
def get_last_word_alphabetically(words):
    last_word = max(words)
    return last_word

# find the longest word
def get_longest_word(words):
    # notice we don't need to write our own function that calls len.
    # we can pass a reference to the len function itself
    longest_word = max(words, key=len)
    return longest_word

# find the shortest word (still using max)
# this is a little sneaky!
def get_shortest_word(words):
    # if we get the negative length, then the largest value will be
    # the negative value closest to 0 (or perhaps even 0, if an
    # empty string was included in the input). we wouldn't usually
    # use max like this (it's confusing when there's a min function
    # we can use instead), but sometimes we need to work within
    # restrictions imposed by other areas of code.
    shortest_word = max(words, key=lambda word: -len(word))
    return shortest_word

# BONUS: now using sorted, put the jumbled sentence into this order:
# a quick brown fox jumps over the laziest dog
# this should still be a list of words, not a single string
# this is a very sneaky!
def get_ordered_words(words):
    # though contrived, this approach could be used to provide an
    # arbitrary ordering for some collection of data. The idea is to
    # have a lookup table of values to use in place of the actual data
    # for the sorting.

    WORD_ORDER = dict(
        a=0, quick=1, brown=2, fox=3, 
        jumps=4, over=5, the=6, laziest=7, dog=8
    )
    
    ordered = sorted(words, key=lambda word: WORD_ORDER[word])
    return ordered

# BONUS BONUS BONUS: back to using max! How can we get the _first_ word
# alphabetically in the list? This one is _very_ sneaky (and
# absolutely not recommended in real code. Just use min!).

# This is very challenging and requires concepts not covered in the
# curriculum! Feel no pressure to attempt this at all!

# we might try to "negate" a string similar to how we were able to
# get the shortest string by negating the length
def negate_string(word):
    # iterate over each letter in the word, converting it to a number
    # (ord gets the numeric representation of a character). Then, just
    # as we did to get the shortest length, negate the resulting number
    # so that larger values are now smaller values. Finally, combine
    # negated values into tuples of numbers, which Python will then
    # compare position by position (just like it does with strings!)
    return tuple(-ord(c) for c in word)

# And while this works when the strings don't have any ties, when there
# _are_ shared letters, this will pick the longer string over the
# shorter string. e.g., in ["a", "abc"], this approach will still 
# favor "abc", since it is longer, and behind the scenes, max is still
# really looking for the largest value

# If we make some assumptions about how max performs the comparison, we
# we can write a class to slot into the algorithm instead. Assuming
# comparisons are performed as `if key(current_best) < key(item):` then
# `key(value)` looks like a constructor call, and `<` is an operator we
# can overload. The constructor can store the value being compared, and
# `<` can get the value from the other (now class-wrapped) value and
# reverse the comparison!
class reverse_lexical:
    def __init__(self, word):
        # when called as reverse_lexical(word), this will store the
        # word to use later
        self.word = word
        
    def __lt__(self, other):
        # when used as `reverse_lexical(w1) < reverse_lexical(w2)`,
        # this makes a new object on the left storing the w1, a new
        # object on the right storing w2, and then calls `__lt__` on
        # the w1 instance, passing the w2 instance. We can the return
        # the result of comparing them in reverse order
        return other.word < self.word

def get_first_word_alphabetically(words):
    # use our new function that "negates" each string by converting it
    # into a tuple of negative numbers. tuples are compared position
    # by position, and so now, each string is "reflected" so that
    # larger letters have become smaller letters. Unfortunately, this
    # doesn't work for partial ties, since tuple comparisons will take
    # longer tuples to be "larger" than shorter tuples when the beginnings
    # tie.
    
    # return max(words, key=negate_string)

    # Instead, we must make use of a custom comparison _class_ that is
    # able to keep track of the _two_ things being compared, rather than
    # acting in isolation on a single value
    return max(words, key=reverse_lexical)

# There is also an adapter method in functools that can build a
# comparison class for us. Definitely firmly in the "follow your curiosity"
# camp.

# def get_first_word_alphabetically(words):
#     from functools import cmp_to_key
#     return max(words, key=cmp_to_key(lambda lhs, rhs: lhs < rhs))

def main():
    assert get_last_word_alphabetically(WORDS) == "the"
    print("get_last_word_alphabetically PASSED!")
    assert get_longest_word(WORDS) == "laziest"
    print("get_longest_word PASSED!")
    assert get_shortest_word(WORDS) == "a"
    print("get_shortest_word PASSED!")

    # BONUS
    assert get_ordered_words(WORDS) == [
        "a", "quick", "brown", "fox", "jumps", 
        "over", "the", "laziest", "dog"
    ]
    print("get_ordered_words PASSED!")
    
    # BONUS BONUS BONUS
    assert get_first_word_alphabetically(WORDS) == "a"
    print("get_first_word_alphabetically PASSED!")

    print("All tests PASSED!")

if __name__ == "__main__":
    main()
