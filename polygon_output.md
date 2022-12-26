# Umbra Deanonymization on polygon

## HEURISTICS 1

reports/results/polygon/
There are `16/66508` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.
This means we have assigned `16` stealth addresses to `4` different addresses. 
This heuristics deanonymized `16`stealth addresses and connected`0` stealth addresses together.  
With this, `16` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `16/33348`**  
**TOTAL connected stealths: `0/33348`**

## HEURISTICS 2

There are `0/66508` addresses who have sent funds to themselves.
This means we have assigned `0` stealth addresses to `0` different addresses,

This heuristics deanonymized `0`stealth addresses and connected`0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `16/33348`**  
**TOTAL connected stealths: `0/33348`**

## HEURISTICS 3

|    |   # of addresses |   with this many txs |
|---:|-----------------:|---------------------:|
|  0 |             7210 |                    1 |
|  1 |             1917 |                    2 |
|  2 |             1714 |                    3 |
|  3 |              585 |                    4 |
|  4 |              436 |                    5 |
|  5 |              334 |                    6 |
|  6 |              254 |                    7 |
|  7 |              122 |                    8 |
|  8 |               92 |                    9 |
|  9 |               87 |                   10 |
| 10 |               83 |                   12 |
| 11 |               76 |                   11 |
| 12 |               68 |                   13 |
| 13 |               38 |                   14 |
| 14 |               27 |                   15 |
| 15 |                8 |                   16 |
| 16 |                7 |                   20 |
| 17 |                7 |                   17 |
| 18 |                6 |                   22 |
| 19 |                4 |                   18 |
| 20 |                3 |                   33 |
| 21 |                3 |                   23 |
| 22 |                3 |                   19 |
| 23 |                2 |                   36 |
| 24 |                2 |                   30 |
| 25 |                2 |                   24 |
| 26 |                2 |                   28 |
| 27 |                2 |                   25 |
| 28 |                2 |                   41 |
| 29 |                2 |                   43 |
| 30 |                1 |                   44 |
| 31 |                1 |                  182 |
| 32 |                1 |                  134 |
| 33 |                1 |                   59 |
| 34 |                1 |                   50 |
| 35 |                1 |                   40 |
| 36 |                1 |                   63 |
| 37 |                1 |                  261 |
| 38 |                1 |                   98 |
| 39 |                1 |                   26 |
| 40 |                1 |                   55 |
| 41 |                1 |                   42 |
| 42 |                1 |                   21 |

Those, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. There are `7210` addresses like this.
From this we have already deanonymized `0` stealth addresses, so there are only `7210` good users.
So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:

We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> 10*.
There are `0` stealths like this out of `5998` stealths.
This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).
Neither one is really good or precise, so we simply just can't tell the underlying address behind a stealth address. Because of that we will connect these addresses together and state that these stealth addresses have common receivers, and with that we made the anonymity set of these stealth addresses a lot smaller since we found some kind of relation among them.
There are `25950` receiver addresses who has a *collection_count* *> 1*, which from `16` stealth addresses have been already deanonymized. However we will include these deanonymized ones to the connections since it carries more information.

This heuristics deanonymized `0`stealth addresses and connected`13111` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `13111` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `16/33348`**  
**TOTAL connected stealths: `13111/33348`**

## HEURISTICS 4

Fees where there's both sender and withdrawal tx: []

No fee was found where there's both sender and withdrawal tx, so this heuristics actually didn't find anything. Based on this it looks like Umbra users use the fees correctly.

This heuristics deanonymized `0`stealth addresses and connected`0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `16/33348`**  
**TOTAL connected stealths: `13111/33348`**

## Summarize

We will merge the deanonymized stealth addresses into the connections and then remove those connections where all of the connected stealth has the *receiver address* (the key)as their *underlying address*.

After the revision, these are the final results:  
**TOTAL deanonymized stealths: `16/33348`**  
**TOTAL connected stealths: `13107/33348`**  
There are `20225` stealth addresses which weren't included in neither heuristics, so the people behind them are the good users of Umbra.

All the results were printed out to **polygon_results.json** file.
