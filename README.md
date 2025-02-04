# Supply-Chain-Case-Study
Real-world supply chain case study solved using mixed-integer programming in Excel and Python, including an interactive map for the proposed solutions. For confidentiality reasons some details will be left out, and data is anonymized. However all of the information to understand and solve the problem will be provided. The scenario solutions are visualized on an interactive map: https://manueltuor.github.io/Supply-Chain-Case-Study/.
<img width="1459" alt="image" src="https://github.com/user-attachments/assets/eaa0c015-5539-4baf-8d1b-013e24129819" />


# Introduction
The case study is about a multinational company that produces in Asia, while serving European markets. The company oversees the assembly to packaging process via contract manufacturers in Asia, cross-dock facilities at airports and ports in Europe, and distribution centers for inventory. Products are then supplied to both major and local retailers for sale to diverse customers. The company aims to balance economic goals with environmental concerns e.g. minimizing operational costs while managing carbon emissions.

The product flow of the company is as follows:
Manufacturers -> Cross-Docks -> Distribution Centers -> Retailers

The supply chain includes two manufacturing facilities situated in Asia. After manufacturing the products, they are routed to three strategically positioned cross-dock facilities at European airports and ports. The network incorporates four distribution centers that serve as central hubs for inventory storage and management. These facilities collectively cater to the demands of end customers through twelve retailers. Furthermore, all products are shipped via air freight for expedited delivery. The ID's of the different supply chain actors are as follows:

Manufacturers: TW, SHA

Cross-Docks: ATVIE, PLGDN, FRCDG

Distribution centers: PED, FR6216, RIX, GMZ

Retailers: FLXXC, ALKFM, KSJER, GXEQH, QAHLE, ISNQE, NAAVF, XGUTS, FLDNI, TWKZB, VWDRE, FFSVQ

The table below explains the data attributes in the given dataset files.
| **ATTRIBUTE**                  | **OWNER**                                              | **DESCRIPTION** |
|--------------------------------|------------------------------------------------------|----------------|
| **SOURCING COST (€)**          | Manufacturer (source)                                | Unit sourcing costs across various manufacturers |
| **HANDLING COST (€)**          | Cross-Deck & Distribution Centres                   | Cost of handling each unit upon receipt/storage in respective locations |
| **DEMAND (UNIT)**              | Retailer                                            | Retailers’ demand |
| **VARIABLE COST (€)**          | New Production (Optional Source)                    | Unit variable cost (per product) for each newly opened facility |
| **OPENING COST (€)**           | New Production (Optional Source)                    | Fixed opening cost for each newly established facility |
| **OPERATIONAL COST (€)**       | New Production (Optional Source)                    | Operational expenses for newly established facilities (optional source) per year |
| **OVERALL CAPACITY (UNIT)**    | New Production Facilities (Optional Source) & DCs   | Maximum available capacity per year at each New Production facility and DC |
| **LATITUDE & LONGITUDE**       | All Locations (Nodes)                               | The distance between nodes should be calculated using latitude and longitude coordinates. |
| **TRANSPORTATION COST/KG-KM (€)** | Air – 0.0114<br>Sea – 0.0017<br>Road – 0.0065 | The estimated average transportation costs for electronic products per kilogram-kilometre. |
| **CO₂-EMISSIONS FACTORS (gCO₂/TONNE-KM)** | Air – 952<br>Sea – 24<br>Road – 73 | Average emissions factors by transportation modes |

In addition product weight is 2.63 kg per unit.

As part of your role in providing analytical support to the company management, you are required to develop a transshipment model that encompasses location and transportation mode decisions to facilitate the analysis of the situation. The following scenarios will guide you in making informed decisions and recommendations.

## Scenario 1: 
To expedite time-to-market, the company currently utilizes air freight for product shipments. Your task is to formulate an efficient distribution plan, incorporating relevant data and input parameters, to address the transshipment challenge. This plan should outline the allocation of products from sources to cross-docks, cross-docks to distribution centres, and distribution centres to retailers.

## Scenario 2: 
To enhance resilience against supply chain disruptions, management wishes to establish new production facilities (Optional Source), close to demand points in Europe. There are six potential locations (HUDTG, CZMCT, IEILG, FIMPF, PLZCA) for establishing a new production facility. Consequently, the product flow within the supply chain is reconfigured as follows: Optional Sources can supply directly to Distribution Centers, thus bypassing Cross-Docks. However, apart from variable production costs, these locations are associated with significant opening and operating costs, but they are expected to reduce transportation costs. Therefore, by considering location decisions your task is to reformulate the transhipment problem developed in Scenario 1 and to investigate the feasibility of opening a production facility.

## Scenario 3:
Recognizing that air freight is both expensive and environmentally unsustainable, the company is proactively investigating alternative strategies to minimize costs and reduce its carbon footprint. Consequently, the management seeks to understand the impact of adopting an alternative transportation mode, encompassing sea freight and road in addition to air freight. It's important to note that the road transportation option is not available for the movement of goods from manufacturers to cross-docks; the only available options are air and sea freight. Although the cost factor plays a key role in the decision-making, the speed of the chosen transportation mode is also crucial for the company. The company has analyzed historical data and discovered that different transportation modes are associated with different additional costs per unit distance, primarily attributable to variations in their transport speed. These additional costs encompass expenses incurred due to stockouts, backorders, penalty costs, and other factors. Internally, the company refers to this category of cost as “slowness cost (𝜋),” and it is estimated for each transportation mode as follows:

• 𝜋 𝑎𝑖𝑟 = 0.00063 € 𝑢𝑛𝑖𝑡/𝑘𝑚

• 𝜋 𝑠𝑒𝑎 = 0.0521 € 𝑢𝑛𝑖𝑡/𝑘𝑚

• 𝜋 𝑟𝑜𝑎𝑑 = 0.00240 € 𝑢𝑛𝑖𝑡/𝑘𝑚

And now, the management wishes to exert more effort into abating its carbon emissions. Please provide suggestions to the compang to make a trade-off between reducing its emissions compared to the current plans (Scenario 1 & 2) and the change in optimizing its allocation plan with a primary focus on minimizing the cost associated with carbon emissions. What is the effect of this new consideration on the allocation plan?

# Solution
All of the different scenario solutions are visualized on the interactive map `index.html` viewable on https://manueltuor.github.io/Supply-Chain-Case-Study/, the paths on the map are color coded according to unit count, and the circles sizes are also proportional to unit count, all the elements can be clicked on for further information. The python script used to create the map is in `map.py`, the raw data is in the `Raw Data` directory, and the Excel solution is in the `Case Study.xlsx` file. This section will provide detailed information about the solution path and results.

## Scenario 1:
In scenario 1 the cost optimal transshipment plan using only air freight is to be determined. Beforehand we will assume that supply meets demand, so that backorder costs do not need to be factored in. To calculate total costs the distances had to be determined first, since the coordinates are given, the distance between two latitude and longitude points can be calculated as follows: 

```python
from math import radians, sin, cos, sqrt, atan2

def distance(lat1, lat2, lon1, lon2):
    R = 6373.0
    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))
    lon1 = radians(float(lon1))
    lon2 = radians(float(lon2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    dist = R * c
    return dist

```
After that the following constraints were set: capacity constraints for the Distribution Centers, demand constraints to ensure demand is met and flow constraints to ensure that in-flow equals out-flow. Finally the optimal total cost was calculated via the Excel solver:

**Cost: 72.2M €**

On the interactive map we can see that all of the product is manufactured in Shanghai, even though sourcing cost in Taiwan is cheaper. This is because the transportation cost, given the bigger distance, outweighs the cheaper sourcing cost.

## Scenario 2:
In scenario 2 there is an option to open production facilities in Europe to reduce cost. The solution is very similar to that of scenario 1. We do need to consider some additional constraints however: capacity constraints for optional sources and choice constraints for optional sources.

**Cost: 59.1M €**

On the interactive map we can see that the 3 optional sources in Helsinki, Warsaw and Budapest are opened, reducing total cost by roughly 13M €. Since the opening cost only needs to be paid once, the total cost for the next year will decrease even further.

## Scenario 3:
For scenario 3 road and sea freight are now possible as well. So the road and sea distances need to be calculated. Road freight is only possible within Europe, the distances and paths were retrieved via the open source osrm API, the routes are in the `Road Routes` folder. For sea freight only locations close to a port were considered, so taking into account the order of transportation only 15 possible routes remain. Since no free API was found, the distances were looked up at https://sea-distances.org and the paths were drawn by hand using https://geojson.io/. The shipping routes can be found in the folder `Shipping Routes`. In addition to cost, CO2 emissions will also be considered in scenario 3.

### Scenario 3.1:
In scenario 3.1 all transportation modes are allowed, but facilities in Europe are not allowed. Since the amount of decision variables increases by a factor of three because of the additional freight options, this problem is only solvable in Excel using the OpenSolver. The problem is modeled similarly to scenario 1 though, with the exception that in- and out-flow from all transportation modes need to be added together in the constraints.

**Cost: 71.6M €**

**CO2 Emissions: 4.8B g/CO2**

So the cost-optimal solution with all transportation modes is slightly cheaper, however the slowness cost is not factored in for scenario 1 so the comparison is unfair. On the interactive map we can see that transportation from Asia to Europe is done via air freight and transportation within Europe via road. This means that road freight is cheaper for shorter distances, and sea freight is never cheaper because of slowness cost. The only exception is one path from Athens were the product is transported via air to a Greek island:
<img width="503" alt="image" src="https://github.com/user-attachments/assets/21e39142-3038-4341-8e57-49bf59c86af7" />

### Scenario 3.2:
In scenario 3.2 we do have the additional option of opening facilities in Europe. Again the cost is minimized and CO2 emission are considered. The OpenSolver yields the following solution:

**Cost: 57.7M €**

**CO2 Emissions: 1.7B g/CO2**

So cost is reduced significantly while emissions go down to roughly one third when allowing production in Europe. This makes sense since facilities in Europe result in smaller distances, which are the main drivers of emissions. On the map we can see that the same 3 facilities as in scenario 2 are opened and the transportation modes are the same as in scenario 3.1.

### Reasonable solution:
The main part of this task is to propose a solution to the management. Now this proposed solution should be somewhere between a min CO2 solution and a min cost solution. So just for reference the min CO2 solution is as follows:

**Cost: 117.7M € (~ 2x more than cost optimal)**

**CO2 Emissions: 0.115B g/CO2 (~ 14x less than cost optimal)**

We can see on the interactive map that there is no air freight in the CO2 optimal solution, since that is the main driver of emissions. Also all European facilities are opened to reduce transportation distances. While emissions are reduced by factor 14, the cost increase of factor 2 is way too high.

<img width="813" alt="image" src="https://github.com/user-attachments/assets/faa57867-47d0-4570-869a-ac14202e589e" />

A reasonable solution must lie somewhere between the cost optimal and CO2 optimal solution. By setting emission constraints, and noting the costs and emissions for several solutions in between the following graph was derived:

<img width="603" alt="image" src="https://github.com/user-attachments/assets/928e7cd7-0075-4efd-bf13-183c6a280791" />

This graph helps understanding the solvers behavior. The min cost solution is in scenario 3.2, where 3 optional facilities are built. Now to further reduce emissions one needs to build more facilities in europe, this results in moderately growing cost. Now when all facilities are built, only shipping will further reduce emissions. However this results in rapidly growing cost as we can see on the graph. This is because shipping has a higher slowness cost and less direct paths compared to the other transportation modes. So the reasonable solution would be to build all facilities in Europe and reduce emissions up to the point where they could only be reduced further by shipping. This would yield the following result:

**Cost: 63.2M € (~ 1.09x more than cost optimal)**

**CO2 Emissions: 0.785B g/CO2 (~ 2.17x less than cost optimal)**

So by increasing cost by roughly 10%, emissions could be reduced to more than half.
<img width="1458" alt="image" src="https://github.com/user-attachments/assets/44b74262-fde8-41d7-9787-d06e40b3329c" />









