# Umbra Deanonymization on polygon

## HEURISTICS 1

There are `15075/91798` withdraw transactions (eth+token) where the receiver address has registrated public keys into the stealth key registry.
This means we have assigned `15075` stealth addresses to `8862` different addresses. 
This heuristics deanonymized `15075` stealth addresses and connected `0` stealth addresses together.  
With this, `15075` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `15075/58454`**  
**TOTAL connected stealths: `0/58454`**

## HEURISTICS 2

There are `670/91798` addresses who have sent funds to themselves.
This means we have assigned `670` stealth addresses to `491` different addresses,

This heuristics deanonymized `670` stealth addresses and connected `0` stealth addresses together.  
With this, `9` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `15084/58454`**  
**TOTAL connected stealths: `0/58454`**

## HEURISTICS 3

|    |   # of addresses |   with this many txs |
|---:|-----------------:|---------------------:|
|  0 |            21363 |                    1 |
|  1 |             3377 |                    2 |
|  2 |             2158 |                    3 |
|  3 |              816 |                    4 |
|  4 |              531 |                    5 |
|  5 |              411 |                    6 |
|  6 |              290 |                    7 |
|  7 |              178 |                    8 |
|  8 |              135 |                    9 |
|  9 |              123 |                   10 |
| 10 |              118 |                   11 |
| 11 |              103 |                   12 |
| 12 |               77 |                   13 |
| 13 |               49 |                   14 |
| 14 |               30 |                   15 |
| 15 |               11 |                   16 |
| 16 |                9 |                   20 |
| 17 |                9 |                   22 |
| 18 |                8 |                   17 |
| 19 |                8 |                   18 |
| 20 |                5 |                   23 |
| 21 |                4 |                   19 |
| 22 |                3 |                   24 |
| 23 |                3 |                   33 |
| 24 |                3 |                   42 |
| 25 |                3 |                   21 |
| 26 |                3 |                   26 |
| 27 |                3 |                   43 |
| 28 |                2 |                   36 |
| 29 |                2 |                   41 |
| 30 |                2 |                   32 |
| 31 |                2 |                   30 |
| 32 |                2 |                   50 |
| 33 |                2 |                   25 |
| 34 |                2 |                   28 |
| 35 |                1 |                   44 |
| 36 |                1 |                   98 |
| 37 |                1 |                   40 |
| 38 |                1 |                   52 |
| 39 |                1 |                   59 |
| 40 |                1 |                  182 |
| 41 |                1 |                  134 |
| 42 |                1 |                  261 |
| 43 |                1 |                   76 |
| 44 |                1 |                   67 |
| 45 |                1 |                   45 |
| 46 |                1 |                   37 |
| 47 |                1 |                  102 |
| 48 |                1 |                   63 |
| 49 |                1 |                   55 |

Those, who have 1 *collection_count* in the result (an address is only used once for withdrawal) look like used the umbra correctly. There are `21363` addresses like this.
From this we have already deanonymized `6786` stealth addresses, so there are only `14577` good users.
So for the others we could say that they have been deanonymized, but it wouldn't be necessarily true since the receivers could be exchange or similar addresses. Because of that we should somehow eliminate these addresses. Sadly there's not really a way to precisely recognize them, so we will do the following:

We will check if there are already deanonymized stealth addresses in the pattern where *collection_count* is *> 10*.
There are `1902` stealths like this out of `8062` stealths.
This is too much so we can't determine those exchange or commerce company addresses based on the size of the pattern. We could either say that all the addresses except the ones with *collection_count* = 1 have been deanonymized or we could say that we will only count as deanonymized the addresses with *collection_count* *<= 5* (just a random number).
Neither one is really good or precise, so we simply just can't tell the underlying address behind a stealth address. Because of that we will connect these addresses together and state that these stealth addresses have common receivers, and with that we made the anonymity set of these stealth addresses a lot smaller since we found some kind of relation among them.
There are `35574` receiver addresses who has a *collection_count* *> 1*, which from `8298` stealth addresses have been already deanonymized. However we will include these deanonymized ones to the connections since it carries more information.

This heuristics deanonymized `0` stealth addresses and connected `29860` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `29860` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `15084/58454`**  
**TOTAL connected stealths: `29860/58454`**

## HEURISTICS 4

Fees where there's both sender and withdrawal tx: [68000000000, 300000000000, 99000000000, 200000000000, 150000000000, 70000000000, 100000000000, 35000000000, 36000000000, 55000000000, 30069999958, 30069999987, 80000000000, 40000000000, 42000000000, 50000000000, 30069999988, 30069999989, 32009999984, 30069999966, 30070000002, 33000000000, 30000000000, 38000000000, 41000000000, 30069999937, 60000000000, 30108799986, 32000000000, 30108799975, 30108799969, 30069999982, 31000000000, 30069999877, 39000000000, 30070000000, 30069999991, 30069999946, 30069999969, 30069999974, 30069999739, 500000000000, 30070000008, 30000000018, 30000000195, 30000000105, 37000000000, 32009999996, 30069999999, 30108800000, 30069999985, 30069999560, 31049699990, 30069999998, 30069999938, 30069999962, 30069999960, 30069999984, 30069999990, 31049699986, 30428706001, 30070000006, 30554999997, 30070000012, 32591999989, 30554999999, 30555000002, 30069999995, 30069999978, 30118208997, 65000000000, 61000000000, 31614239989, 30069999965, 52000000000, 30069999986, 30069999980, 30070000001, 45000000000, 31039999957, 30069998024, 30069999942, 30108799987, 30070000003, 66000000000, 77000000000, 88000000000, 30070000007, 30099955544, 30069999808, 30069999932, 30069999992, 30069999981, 30166999998, 800000000000, 32010000000, 30555000000, 30070000038, 30069999737, 30069999949, 32591999991, 30069999897, 31040000002, 31040000001, 31331000000, 44000000000, 47000000000, 56000000000, 30069999975, 34000000000, 30069999983, 35890000000, 30069999964, 30981955189, 30108799999, 30069999943, 30069999944, 30069999882, 30069999781, 38799999977, 30069999434, 30985248334, 30069999861, 32931499990, 30985248340, 49000000000, 32320400000, 30118209000, 31039999982, 46000000000, 48000000000, 30419200000, 30069999968, 30070000403, 30069999800, 30069999957, 30428705986, 30069999979, 30742403977, 30069999976, 30069999891, 30069999919, 30069999977, 30069999935, 30069999959, 30069999736, 30118209004, 30069999963, 31049699982, 30499706298, 30069999925, 30069999970, 30428705996, 30236818512, 30626294981, 30069999971, 30070000014, 30555000054, 30108800009, 30069999795, 30069999887, 30013769095, 30070000081, 30069999972, 30069999413, 31049699964, 30070000059, 38799999985, 30069999930, 30069999816, 30099955540, 98000000000, 30069999951, 30069999961, 30069999954, 30118208983, 30069999664, 75000000000, 72000000000, 115000000000, 30069999750, 30069999805, 30069999605, 30069999832, 30069999581, 30069999952, 30069999953, 30069999945, 160000000000, 130000000000, 95000000000, 90000000000, 92000000000, 222000000000, 111000000000, 120000000000, 110000000000, 71000000000, 250000000000, 30069999904, 133000000000, 85000000000, 170000000000, 155000000000, 97000000000, 59000000000, 30069999014, 30118208977, 30069999950, 30069999467, 30069999869, 30200000000, 30108800002, 30069999936, 30069999920, 30069999531, 30069999898, 30069999896, 30069999823, 31049700003, 30675395884, 31049700016, 31049699970, 32931500032, 31369800002, 32100000000, 32010000020, 30665812801, 30555000015, 31369800001, 30070000057, 30069999933, 30118209001, 30089400000, 30118209014, 400000000000, 30010000000, 30555000016, 30555000017, 33490626974, 30611721174, 30225199980, 260000000000]

No fee was found where there's both sender and withdrawal tx, so this heuristics actually didn't find anything. Based on this it looks like Umbra users use the fees correctly.

This heuristics deanonymized `0` stealth addresses and connected `0` stealth addresses together.  
With this, `0` new stealth addresses have been added to the deanonymization set and `0` new stealth addresses have been connected together.  

**TOTAL deanonymized stealths: `15084/58454`**  
**TOTAL connected stealths: `29860/58454`**

## Summarize

We will merge the deanonymized stealth addresses into the connections and then remove those connections where all of the connected stealth has the *receiver address* (the key) as their *underlying address* (so if all of the included stealths are deanonymized as the receiver).

After the revision, these are the final results:  
**TOTAL deanonymized stealths: `15084/58454`**  
**TOTAL connected stealths: `20993/58454`**  
There are `22377` stealth addresses which weren't included in neither heuristics, so the people behind them are the good users of Umbra.

All the results were printed out to **polygon_results.json** file.
