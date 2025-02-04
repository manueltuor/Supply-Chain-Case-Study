# Supply-Chain-Case-Study
Real-world supply chain case study solved using mixed-integer programming in Excel and Python, including an interactive map for the proposed solutions. For confidentiality reasons some details will be left out, and data is anonymized. However all of the information to understand and solve the problem will be provided.

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



