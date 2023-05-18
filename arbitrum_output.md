# Umbra Deanonymization on arbitrum

## HEURISTICS 1

There are `12488/19965` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.
This means we have assigned `12488` stealth addresses to `6817` different addresses. 
This heuristics deanonymized `12488` stealth addresses and connected `0` stealth addresses together.  
With this, `12488` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `12488/19033`**  
**TOTAL connected stealths: `0/19033`**

## HEURISTICS 2

There are `356/19965` addresses who have sent funds to themselves.
This means we have assigned `356` stealth addresses to `247` different addresses,

This heuristics deanonymized `356` stealth addresses and connected `0` stealth addresses together.  
With this, `25` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `12513/19033`**  
**TOTAL connected stealths: `0/19033`**

## HEURISTICS 3

|    |   # of addresses |   with this many txs |
|---:|-----------------:|---------------------:|
|  0 |             7020 |                    1 |
|  1 |             1906 |                    2 |
|  2 |              710 |                    3 |
|  3 |              300 |                    4 |
|  4 |              210 |                    5 |
|  5 |              127 |                    6 |
|  6 |               82 |                    7 |
|  7 |               42 |                    8 |
|  8 |               23 |                    9 |
|  9 |               17 |                   10 |
| 10 |                8 |                   13 |
| 11 |                7 |                   19 |
| 12 |                7 |                   12 |
| 13 |                6 |                   11 |
| 14 |                4 |                   17 |
| 15 |                3 |                   14 |
| 16 |                3 |                   15 |
| 17 |                2 |                   20 |
| 18 |                2 |                   16 |
| 19 |                1 |                   45 |
| 20 |                1 |                   32 |
| 21 |                1 |                   24 |
| 22 |                1 |                   39 |
| 23 |                1 |                   48 |
| 24 |                1 |                   18 |
| 25 |                1 |                   62 |
| 26 |                1 |                   50 |
| 27 |                1 |                   23 |
| 28 |                1 |                   28 |
| 29 |                1 |                  481 |

Those, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. There are `7020` addresses like this.
From this we have already deanonymized `4358` stealth addresses, so there are only `2662` good users.
So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:

We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> 10*.
There are `682` stealths like this out of `1464` stealths.
This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).
Neither one is really good or precise, so we simply just can't tell the underlying address behind a stealth address. Because of that we will connect these addresses together and state that these stealth addresses have common receivers, and with that we made the anonymity set of these stealth addresses a lot smaller since we found some kind of relation among them.
There are `11705` receiver addresses who has a *collection_count* *> 1*, which from `8155` stealth addresses have been already deanonymized. However we will include these deanonymized ones to the connections since it carries more information.

This heuristics deanonymized `0` stealth addresses and connected `10490` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `10490` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `12513/19033`**  
**TOTAL connected stealths: `10490/19033`**

## HEURISTICS 4

Fees where there's both sender and withdrawal tx: [100000000]
[100000000]
so this heuristics actually didn't find anything. Based on this it looks like Umbra users use the fees correctly.

This heuristics deanonymized `0` stealth addresses and connected `0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `12513/19033`**  
**TOTAL connected stealths: `10490/19033`**

## Summarize

We will merge the deanonymized stealth addresses into the connections and then remove those connections where all of the connected stealth has the *receiver address* (the key) as their *underlying address* (so if all of the included stealths are deanonymized as the receiver).

After the revision, these are the final results:  
**TOTAL deanonymized stealths: `12513/19033`**  
**TOTAL connected stealths: `3666/19033`**  
There are `2854` stealth addresses which weren't included in neither heuristics, so the people behind them are the good users of Umbra.

All the results were printed out to **arbitrum_results.json** file.
