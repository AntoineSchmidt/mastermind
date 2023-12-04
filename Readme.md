# Solving Mastermind
This projects implements the [min-max algorithm from Donal Knuth (1977)](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm) with a modification.

1. Create the set S of all possible codes (1111, 1112 ... 6665, 6666)
2. Start with initial guess 1122 (Knuth gives examples showing that this algorithm using other first guesses such as 1123, 1234 does not win in five tries on every code)
3. Play the guess to get a response of coloured and white pegs.\
If the response is four colored pegs, the game is won, the algorithm terminates.\
Otherwise, remove from S any code that would not give the same response if it (the guess) were the code.
4. Apply minimax technique to find a next guess as follows:\
For each possible guess, that is, any unused code of the 1296 not just those in S, calculate how many possibilities in S would be eliminated for each possible colored/white peg score. The score of a guess is the minimum number of possibilities it might eliminate from S. A single pass through S for each unused code of the 1296 will provide a hit count for each coloured/white peg score found; the coloured/white peg score with the highest hit count will eliminate the fewest possibilities; calculate the score of a guess by using "minimum eliminated" = "count of elements in S" - (minus) "highest hit count". From the set of guesses with the maximum score, select one as the next guess, choosing a member of S whenever possible.
5. Repeat from step 3.


## Modification
As the opponent does not actively minimize the reward of each guess, I modified step 4 to subselect the resulting highest-scoring guess set by the highest number of possible unique answers.\
In other words, if there are, for example, 2 next guesses with the highest same value score by Knuth, the guess with the highest number of possible unique answers gets selected, so that if the guess doesn't score the worst answer (the answer having the biggest set size), the algorithm is better off (because the average set size is smaller).\
This modification allows step 4 to be used for the initial guess, resulting in codes with two double colors in a 4-peg six-color game.