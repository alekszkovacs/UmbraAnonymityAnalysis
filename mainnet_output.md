# Umbra Deanonymization on mainnet

## HEURISTICS 1

There are `4591/8885` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.
This means we have assigned `4591` stealth addresses to `2887` different addresses. From these `1440` has ens address.

This heuristics deanonymized `4591` stealth addresses and connected `0` stealth addresses together.  
With this, `4591` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `4591/8192`**  
**TOTAL connected stealths: `0/8192`**

## HEURISTICS 2

There are `240/8885` addresses who have sent funds to themselves.
This means we have assigned `240` stealth addresses to `213` different addresses,
which from `0` has ens address.

This heuristics deanonymized `240` stealth addresses and connected `0` stealth addresses together.  
With this, `17` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `4608/8192`**  
**TOTAL connected stealths: `0/8192`**

## HEURISTICS 3

|    |   # of addresses |   with this many txs |
|---:|-----------------:|---------------------:|
|  0 |             4096 |                    1 |
|  1 |             1011 |                    2 |
|  2 |              243 |                    3 |
|  3 |               84 |                    4 |
|  4 |               47 |                    5 |
|  5 |               25 |                    6 |
|  6 |               11 |                    7 |
|  7 |               11 |                    8 |
|  8 |                6 |                    9 |
|  9 |                5 |                   10 |
| 10 |                4 |                   12 |
| 11 |                3 |                   11 |
| 12 |                2 |                   14 |
| 13 |                2 |                   18 |
| 14 |                1 |                   24 |
| 15 |                1 |                   23 |
| 16 |                1 |                   35 |
| 17 |                1 |                   38 |

Those, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. There are `4096` addresses like this.
From this we have already deanonymized `1906` stealth addresses, so there are only `2190` good users.
So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:

We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> 10*.
There are `121` stealths like this out of `265` stealths.
This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).
Neither one is really good or precise, so we simply just can't tell the underlying address behind a stealth address. Because of that we will connect these addresses together and state that these stealth addresses have common receivers, and with that we made the anonymity set of these stealth addresses a lot smaller since we found some kind of relation among them.
There are `4006` receiver addresses who has a *collection_count* *> 1*, which from `2702` stealth addresses have been already deanonymized. However we will include these deanonymized ones to the connections since it carries more information.

This heuristics deanonymized `0` stealth addresses and connected `5554` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `5554` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `4608/8192`**  
**TOTAL connected stealths: `5554/8192`**

## HEURISTICS 4

Fees where there's both sender and withdrawal tx: [4000000000, 3000000000, 2000000000, 5000000000, 6000000000, 9000000000, 10000000000, 31000000000, 41000000000, 18000000000]

Sadly all of the fees are some rounded values and we definitely can't say that they are unique, so this heuristics actually didn't find anything. Based on this it looks like Umbra users use the fees correctly.

This heuristics deanonymized `0` stealth addresses and connected `0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `4608/8192`**  
**TOTAL connected stealths: `5554/8192`**

## Summarize

We will merge the deanonymized stealth addresses into the connections and then remove those connections where all of the connected stealth has the *receiver address* (the key) as their *underlying address* (so if all of the included stealths are deanonymized as the receiver).

After the revision, these are the final results:  
**TOTAL deanonymized stealths: `4608/8192`**  
**TOTAL connected stealths: `2656/8192`**  
There are `928` stealth addresses which weren't included in neither heuristics, so the people behind them are the good users of Umbra.

All the results were printed out to **mainnet_results.json** file.
