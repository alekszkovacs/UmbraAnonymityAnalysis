# Umbra Deanonymization

## HEURISTICS 1

There are `4209/7614` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.
This means we have assigned `4209` stealth addresses to `2700` different addresses, which from `1374` has ens address.

This heuristics deanonymized `4209` stealth addresses with high and `0` with low certainty.  
With this, `4209` new stealth addresses with high and `0` with low certainty have been added to the deanonymization set.

**TOTAL with high certainty: `4209/7221`**  
**TOTAL with low certainty: `0/7221`**

## HEURISTICS 2

There are `204/7614` addresses who have sent funds to themselves.
This means we have assigned `204` stealth addresses to `182` different addresses,
which from `0` has ens address.

This heuristics deanonymized `204` stealth addresses with high and `0` with low certainty.  
With this, `15` new stealth addresses with high and `0` with low certainty have been added to the deanonymization set.

**TOTAL with high certainty: `4224/7221`**  
**TOTAL with low certainty: `0/7221`**

## HEURISTICS 3

|    |   # of addresses |   with this many txs |
|---:|-----------------:|---------------------:|
|  0 |             3623 |                    1 |
|  1 |              827 |                    2 |
|  2 |              204 |                    3 |
|  3 |               75 |                    4 |
|  4 |               46 |                    5 |
|  5 |               15 |                    6 |
|  6 |               11 |                    7 |
|  7 |               10 |                    8 |
|  8 |                4 |                   12 |
|  9 |                4 |                   10 |
| 10 |                3 |                    9 |
| 11 |                3 |                   11 |
| 12 |                1 |                   13 |
| 13 |                1 |                   18 |
| 14 |                1 |                   14 |
| 15 |                1 |                   24 |
| 16 |                1 |                   23 |
| 17 |                1 |                   35 |
| 18 |                1 |                   38 |

Those, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. There are `3623` addresses like this.
From this we have already deanonymized `1832` stealth addresses, so there are only `1791` good users.
So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:

We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> 10*.
There are `120` stealths like this out of `246` stealths.
This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).
Neither one is really good or precise, so we will introduce a new unit and say that these addresses are deanonymized but with a lower certainty.
There are `3356` addresses who has a *collection_count* *> 1*, which from `964` haven't been already deanonymized. So these are the newly deanonymized with lower certainty.

This heuristics deanonymized `0` stealth addresses with high and `964` with low certainty.  
With this, `0` new stealth addresses with high and `964` with low certainty have been added to the deanonymization set.

**TOTAL with high certainty: `4224/7221`**  
**TOTAL with low certainty: `964/7221`**

## HEURISTICS 4

Fees where there's both sender and withdrawal txs: [4000000000, 3000000000, 2000000000, 5000000000, 6000000000, 9000000000, 10000000000, 31000000000, 41000000000, 18000000000]

This heuristics deanonymized `0` stealth addresses with high and `0` with low certainty.  
With this, `0` new stealth addresses with high and `0` with low certainty have been added to the deanonymization set.

**TOTAL with high certainty: `4224/7221`**  
**TOTAL with low certainty: `964/7221`**
