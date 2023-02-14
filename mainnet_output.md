# Umbra Deanonymization on mainnet

## HEURISTICS 1

There are `4648/9247` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.
This means we have assigned `4648` stealth addresses to `2897` different addresses. From these `1441` has ens address.

This heuristics deanonymized `4648` stealth addresses and connected `0` stealth addresses together.  
With this, `4648` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `4648/8535`**  
**TOTAL connected stealths: `0/8535`**

## HEURISTICS 2

There are `247/9247` addresses who have sent funds to themselves.
This means we have assigned `247` stealth addresses to `216` different addresses,
which from `0` has ens address.

This heuristics deanonymized `247` stealth addresses and connected `0` stealth addresses together.  
With this, `20` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `4668/8535`**  
**TOTAL connected stealths: `0/8535`**

## HEURISTICS 3

|    |   # of addresses |   with this many txs |
|---:|-----------------:|---------------------:|
|  0 |             4241 |                    1 |
|  1 |             1049 |                    2 |
|  2 |              251 |                    3 |
|  3 |               89 |                    4 |
|  4 |               51 |                    5 |
|  5 |               26 |                    6 |
|  6 |               12 |                    8 |
|  7 |               11 |                    7 |
|  8 |                7 |                   10 |
|  9 |                6 |                   11 |
| 10 |                5 |                    9 |
| 11 |                4 |                   12 |
| 12 |                2 |                   18 |
| 13 |                2 |                   14 |
| 14 |                1 |                   24 |
| 15 |                1 |                   23 |
| 16 |                1 |                   35 |
| 17 |                1 |                   38 |

Those, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. There are `4241` addresses like this.
From this we have already deanonymized `1905` stealth addresses, so there are only `2336` good users.
So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:

We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> 10*.
There are `132` stealths like this out of `298` stealths.
This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).
Neither one is really good or precise, so we simply just can't tell the underlying address behind a stealth address. Because of that we will connect these addresses together and state that these stealth addresses have common receivers, and with that we made the anonymity set of these stealth addresses a lot smaller since we found some kind of relation among them.
There are `4204` receiver addresses who has a *collection_count* *> 1*, which from `2763` stealth addresses have been already deanonymized. However we will include these deanonymized ones to the connections since it carries more information.

This heuristics deanonymized `0` stealth addresses and connected `5760` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `5760` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `4668/8535`**  
**TOTAL connected stealths: `5760/8535`**

## HEURISTICS 4

Fees where there's both sender and withdrawal tx: [4000000000, 3000000000, 2000000000, 5000000000, 6000000000, 9000000000, 10000000000, 31000000000, 41000000000, 50000000000, 20000000000, 18000000000, 16000000000]

Sadly all of the fees are some rounded values and we definitely can't say that they are unique, so this heuristics actually didn't find anything. Based on this it looks like Umbra users use the fees correctly.

This heuristics deanonymized `0` stealth addresses and connected `0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `4668/8535`**  
**TOTAL connected stealths: `5760/8535`**

## Summarize

We will merge the deanonymized stealth addresses into the connections and then remove those connections where all of the connected stealth has the *receiver address* (the key) as their *underlying address* (so if all of the included stealths are deanonymized as the receiver).

After the revision, these are the final results:  
**TOTAL deanonymized stealths: `4668/8535`**  
**TOTAL connected stealths: `2849/8535`**  
There are `1018` stealth addresses which weren't included in neither heuristics, so the people behind them are the good users of Umbra.

All the results were printed out to **mainnet_results.json** file.
