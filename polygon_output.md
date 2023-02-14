# Umbra Deanonymization on polygon

## HEURISTICS 1

There are `16/66920` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.
This means we have assigned `16` stealth addresses to `4` different addresses. 
This heuristics deanonymized `16` stealth addresses and connected `0` stealth addresses together.  
With this, `16` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `16/33576`**  
**TOTAL connected stealths: `0/33576`**

## HEURISTICS 2

There are `0/66920` addresses who have sent funds to themselves.
This means we have assigned `0` stealth addresses to `0` different addresses,

This heuristics deanonymized `0` stealth addresses and connected `0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `16/33576`**  
**TOTAL connected stealths: `0/33576`**

## HEURISTICS 3

|    |   # of addresses |   with this many txs |
|---:|-----------------:|---------------------:|
|  0 |             7318 |                    1 |
|  1 |             1928 |                    2 |
|  2 |             1722 |                    3 |
|  3 |              585 |                    4 |
|  4 |              434 |                    5 |
|  5 |              336 |                    6 |
|  6 |              251 |                    7 |
|  7 |              125 |                    8 |
|  8 |               90 |                   10 |
|  9 |               89 |                    9 |
| 10 |               83 |                   12 |
| 11 |               76 |                   11 |
| 12 |               68 |                   13 |
| 13 |               39 |                   14 |
| 14 |               26 |                   15 |
| 15 |                8 |                   16 |
| 16 |                7 |                   17 |
| 17 |                6 |                   20 |
| 18 |                6 |                   22 |
| 19 |                5 |                   18 |
| 20 |                4 |                   23 |
| 21 |                3 |                   33 |
| 22 |                2 |                   21 |
| 23 |                2 |                   28 |
| 24 |                2 |                   24 |
| 25 |                2 |                   36 |
| 26 |                2 |                   30 |
| 27 |                2 |                   25 |
| 28 |                2 |                   41 |
| 29 |                2 |                   19 |
| 30 |                2 |                   43 |
| 31 |                1 |                   44 |
| 32 |                1 |                  182 |
| 33 |                1 |                  134 |
| 34 |                1 |                   59 |
| 35 |                1 |                   50 |
| 36 |                1 |                   40 |
| 37 |                1 |                   63 |
| 38 |                1 |                  261 |
| 39 |                1 |                   98 |
| 40 |                1 |                   26 |
| 41 |                1 |                   55 |
| 42 |                1 |                   42 |

Those, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. There are `7318` addresses like this.
From this we have already deanonymized `0` stealth addresses, so there are only `7318` good users.
So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:

We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> 10*.
There are `0` stealths like this out of `6020` stealths.
This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).
Neither one is really good or precise, so we simply just can't tell the underlying address behind a stealth address. Because of that we will connect these addresses together and state that these stealth addresses have common receivers, and with that we made the anonymity set of these stealth addresses a lot smaller since we found some kind of relation among them.
There are `26026` receiver addresses who has a *collection_count* *> 1*, which from `16` stealth addresses have been already deanonymized. However we will include these deanonymized ones to the connections since it carries more information.

This heuristics deanonymized `0` stealth addresses and connected `13239` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `13239` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `16/33576`**  
**TOTAL connected stealths: `13239/33576`**

## HEURISTICS 4

Fees where there's both sender and withdrawal tx: []

No fee was found where there's both sender and withdrawal tx, so this heuristics actually didn't find anything. Based on this it looks like Umbra users use the fees correctly.

This heuristics deanonymized `0` stealth addresses and connected `0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `16/33576`**  
**TOTAL connected stealths: `13239/33576`**

## Summarize

We will merge the deanonymized stealth addresses into the connections and then remove those connections where all of the connected stealth has the *receiver address* (the key) as their *underlying address* (so if all of the included stealths are deanonymized as the receiver).

After the revision, these are the final results:  
**TOTAL deanonymized stealths: `16/33576`**  
**TOTAL connected stealths: `13235/33576`**  
There are `20325` stealth addresses which weren't included in neither heuristics, so the people behind them are the good users of Umbra.

All the results were printed out to **polygon_results.json** file.
