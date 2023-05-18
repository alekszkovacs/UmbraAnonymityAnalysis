# Umbra Deanonymization on optimism

## HEURISTICS 1

There are `8391/16043` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.
This means we have assigned `8391` stealth addresses to `4858` different addresses. 
This heuristics deanonymized `8391` stealth addresses and connected `0` stealth addresses together.  
With this, `8391` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `8391/15963`**  
**TOTAL connected stealths: `0/15963`**

## HEURISTICS 2

There are `135/16043` addresses who have sent funds to themselves.
This means we have assigned `135` stealth addresses to `102` different addresses,

This heuristics deanonymized `135` stealth addresses and connected `0` stealth addresses together.  
With this, `12` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `8403/15963`**  
**TOTAL connected stealths: `0/15963`**

## HEURISTICS 3

|    |   # of addresses |   with this many txs |
|---:|-----------------:|---------------------:|
|  0 |             7661 |                    1 |
|  1 |             1167 |                    2 |
|  2 |              545 |                    3 |
|  3 |              337 |                    4 |
|  4 |              127 |                    5 |
|  5 |               54 |                    6 |
|  6 |               28 |                    7 |
|  7 |               11 |                    8 |
|  8 |               10 |                    9 |
|  9 |                9 |                   11 |
| 10 |                7 |                   10 |
| 11 |                5 |                   12 |
| 12 |                3 |                   16 |
| 13 |                3 |                   24 |
| 14 |                3 |                   29 |
| 15 |                2 |                   28 |
| 16 |                2 |                   18 |
| 17 |                2 |                   14 |
| 18 |                2 |                   23 |
| 19 |                2 |                   13 |
| 20 |                2 |                   48 |
| 21 |                2 |                   30 |
| 22 |                2 |                   15 |
| 23 |                1 |                   35 |
| 24 |                1 |                  149 |
| 25 |                1 |                   50 |
| 26 |                1 |                   80 |
| 27 |                1 |                   20 |
| 28 |                1 |                   25 |
| 29 |                1 |                   34 |
| 30 |                1 |                   52 |
| 31 |                1 |                   31 |
| 32 |                1 |                   37 |
| 33 |                1 |                   19 |
| 34 |                1 |                  173 |
| 35 |                1 |                   22 |
| 36 |                1 |                   26 |

Those, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. There are `7661` addresses like this.
From this we have already deanonymized `3324` stealth addresses, so there are only `4337` good users.
So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:

We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> 10*.
There are `774` stealths like this out of `1497` stealths.
This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).
Neither one is really good or precise, so we simply just can't tell the underlying address behind a stealth address. Because of that we will connect these addresses together and state that these stealth addresses have common receivers, and with that we made the anonymity set of these stealth addresses a lot smaller since we found some kind of relation among them.
There are `8217` receiver addresses who has a *collection_count* *> 1*, which from `5079` stealth addresses have been already deanonymized. However we will include these deanonymized ones to the connections since it carries more information.

This heuristics deanonymized `0` stealth addresses and connected `10000` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `10000` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `8403/15963`**  
**TOTAL connected stealths: `10000/15963`**

## HEURISTICS 4

Fees where there's both sender and withdrawal tx: []
[]
so this heuristics actually didn't find anything. Based on this it looks like Umbra users use the fees correctly.

This heuristics deanonymized `0` stealth addresses and connected `0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `8403/15963`**  
**TOTAL connected stealths: `10000/15963`**

## Summarize

We will merge the deanonymized stealth addresses into the connections and then remove those connections where all of the connected stealth has the *receiver address* (the key) as their *underlying address* (so if all of the included stealths are deanonymized as the receiver).

After the revision, these are the final results:  
**TOTAL deanonymized stealths: `8403/15963`**  
**TOTAL connected stealths: `5136/15963`**  
There are `2424` stealth addresses which weren't included in neither heuristics, so the people behind them are the good users of Umbra.

All the results were printed out to **optimism_results.json** file.
