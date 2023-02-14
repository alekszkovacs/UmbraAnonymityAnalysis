# Umbra Deanonymization on optimism

## HEURISTICS 1

There are `0/170` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.
This means we have assigned `0` stealth addresses to `0` different addresses. 
This heuristics deanonymized `0` stealth addresses and connected `0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `0/90`**  
**TOTAL connected stealths: `0/90`**

## HEURISTICS 2

There are `0/170` addresses who have sent funds to themselves.
This means we have assigned `0` stealth addresses to `0` different addresses,

This heuristics deanonymized `0` stealth addresses and connected `0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `0/90`**  
**TOTAL connected stealths: `0/90`**

## HEURISTICS 3

|    |   # of addresses |   with this many txs |
|---:|-----------------:|---------------------:|
|  0 |               48 |                    1 |
|  1 |                2 |                    2 |
|  2 |                1 |                    3 |
|  3 |                1 |                    6 |
|  4 |                1 |                    5 |
|  5 |                1 |                    4 |
|  6 |                1 |                   10 |

Those, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. There are `48` addresses like this.
From this we have already deanonymized `0` stealth addresses, so there are only `48` good users.
So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:

We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> 10*.
There are `0` stealths like this out of `0` stealths.
This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).
Neither one is really good or precise, so we simply just can't tell the underlying address behind a stealth address. Because of that we will connect these addresses together and state that these stealth addresses have common receivers, and with that we made the anonymity set of these stealth addresses a lot smaller since we found some kind of relation among them.
There are `32` receiver addresses who has a *collection_count* *> 1*, which from `0` stealth addresses have been already deanonymized. However we will include these deanonymized ones to the connections since it carries more information.

This heuristics deanonymized `0` stealth addresses and connected `55` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `55` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `0/90`**  
**TOTAL connected stealths: `55/90`**

## HEURISTICS 4

Fees where there's both sender and withdrawal tx: []
[]
so this heuristics actually didn't find anything. Based on this it looks like Umbra users use the fees correctly.

This heuristics deanonymized `0` stealth addresses and connected `0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `0/90`**  
**TOTAL connected stealths: `55/90`**

## Summarize

We will merge the deanonymized stealth addresses into the connections and then remove those connections where all of the connected stealth has the *receiver address* (the key) as their *underlying address* (so if all of the included stealths are deanonymized as the receiver).

After the revision, these are the final results:  
**TOTAL deanonymized stealths: `0/90`**  
**TOTAL connected stealths: `55/90`**  
There are `35` stealth addresses which weren't included in neither heuristics, so the people behind them are the good users of Umbra.

All the results were printed out to **optimism_results.json** file.
