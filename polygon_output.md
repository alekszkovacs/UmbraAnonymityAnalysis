# Umbra Deanonymization

## HEURISTICS 1

There are `15/65137` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.
This means we have assigned `15` stealth addresses to `4` different addresses.

This heuristics deanonymized `15` stealth addresses with high and `0` with low certainty.  
With this, `15` new stealth addresses with high and `0` with low certainty have been added to the deanonymization set.

**TOTAL with high certainty: `15/65137`**  
**TOTAL with low certainty: `0/65137`**

## HEURISTICS 2

There are `0/65137` addresses who have sent funds to themselves.
This means we have assigned `0` stealth addresses to `0` different addresses,

This heuristics deanonymized `0` stealth addresses with high and `0` with low certainty.  
With this, `0` new stealth addresses with high and `0` with low certainty have been added to the deanonymization set.

**TOTAL with high certainty: `15/65137`**  
**TOTAL with low certainty: `0/65137`**

## HEURISTICS 3

|    |   # of addresses |   with this many txs |
|---:|-----------------:|---------------------:|
|  0 |             7004 |                    1 |
|  1 |             1793 |                    2 |
|  2 |             1716 |                    3 |
|  3 |              580 |                    4 |
|  4 |              428 |                    5 |
|  5 |              340 |                    6 |
|  6 |              245 |                    7 |
|  7 |              121 |                    8 |
|  8 |               88 |                    9 |
|  9 |               88 |                   10 |
| 10 |               83 |                   12 |
| 11 |               74 |                   11 |
| 12 |               69 |                   13 |
| 13 |               34 |                   14 |
| 14 |               28 |                   15 |
| 15 |                9 |                   16 |
| 16 |                7 |                   17 |
| 17 |                5 |                   22 |
| 18 |                5 |                   19 |
| 19 |                4 |                   20 |
| 20 |                3 |                   33 |
| 21 |                3 |                   23 |
| 22 |                3 |                   18 |
| 23 |                2 |                   41 |
| 24 |                2 |                   25 |
| 25 |                2 |                   26 |
| 26 |                2 |                   24 |
| 27 |                2 |                   43 |
| 28 |                2 |                   21 |
| 29 |                1 |                   27 |
| 30 |                1 |                   36 |
| 31 |                1 |                   98 |
| 32 |                1 |                   55 |
| 33 |                1 |                   30 |
| 34 |                1 |                   59 |
| 35 |                1 |                   40 |
| 36 |                1 |                   28 |
| 37 |                1 |                   44 |
| 38 |                1 |                  182 |
| 39 |                1 |                  134 |
| 40 |                1 |                   50 |
| 41 |                1 |                   63 |
| 42 |                1 |                  261 |
| 43 |                1 |                   42 |

Those, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. There are `7004` addresses like this.
From this we have already deanonymized `1` stealth addresses, so there are only `7003` good users.
So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:

We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> 10*.
There are `0` stealths like this out of `5882` stealths.
This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).
Neither one is really good or precise, so we will introduce a new unit and say that these addresses are deanonymized but with a lower certainty.
There are `25471` addresses who has a *collection_count* *> 1*, which from `25457` haven't been already deanonymized. So these are the newly deanonymized with lower certainty.

This heuristics deanonymized `0` stealth addresses with high and `25457` with low certainty.  
With this, `0` new stealth addresses with high and `25454` with low certainty have been added to the deanonymization set.

**TOTAL with high certainty: `15/65137`**  
**TOTAL with low certainty: `25454/65137`**

## HEURISTICS 4

Fees where there's both sender and withdrawal txs: []

This heuristics deanonymized `0` stealth addresses with high and `0` with low certainty.  
With this, `0` new stealth addresses with high and `0` with low certainty have been added to the deanonymization set.

**TOTAL with high certainty: `15/65137`**  
**TOTAL with low certainty: `25454/65137`**
