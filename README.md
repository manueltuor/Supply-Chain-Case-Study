# Supply-Chain-Case-Study
Real-world supply chain case study solved using mixed-integer programming in Excel and Python, including an interactive map for the proposed solutions.

# Introduction
T-Nova Global Electronics (TGE) is a multinational firm specializing in high-tech electronics, primarily serving European markets. Utilizing contract manufacturers, TGE oversees the assembly to packaging process, utilizing cross-dock facilities at airports and ports, and distribution centers for inventory. Products are then supplied to both major and local retailers for sale to diverse customers including individuals, businesses, and government entities. TGE focuses on product reliability, customer service, and after-sales support. However, TGE faces challenges in balancing economic goals with environmental concerns, particularly in minimizing operational costs while managing carbon emissions. To address this, TGE is exploring a detailed analysis of its supply chain network, considering both operational efficiency and environmental impact.

The current product flow and transportation mode of TGE is visualized as follows:
<img width="512" alt="image" src="https://github.com/user-attachments/assets/31bc639b-9656-4d3f-b699-0a1b58213050" />

TGE's supply chain includes two manufacturing facilities situated in Asia. After manufacturing the products, they are routed to three strategically positioned cross-dock facilities at European airports and ports. The network incorporates four distribution centers (DCs) that serve as central hubs for inventory storage and management. These facilities collectively cater to the demands of end customers through twelve retailers. Furthermore, all products are shipped via air freight for expedited delivery. Please retrieve the information on relevant manufacturers, cross docks, distribution centers, and retailers from the given dataset, with the IDs.

Manufacturers: TW, SHA

Cross docks: ATVIE, PLGDN, FRCDG

Distribution centers: PED, FR6216, RIX, GMZ

Retailers: FLXXC, ALKFM, KSJER, GXEQH, QAHLE, ISNQE, NAAVF, XGUTS, FLDNI, TWKZB, ,VWDRE, FFSVQ

The table below explains the data attributes in the given dataset files.
<img width="509" alt="image" src="https://github.com/user-attachments/assets/09da36ac-e452-4e5b-8627-f60ad9983c14" />

As part of your role in providing analytical support to TGE's management, you are required to develop a transshipment model that encompasses location and transportation mode decisions to facilitate the analysis of the situation. The following scenarios will guide you in making informed decisions and recommendations.

## Scenario 1: 
To expedite time-to-market, TGE currently utilizes air freight for product shipments. Your task is to formulate an efficient distribution plan, incorporating relevant data and input parameters, to address the transshipment challenge. This plan should outline the allocation of products from sources to cross-docks, cross-docks to distribution centres, and distribution centres to retailers.

## Scenario 2: 
To enhance resilience against supply chain disruptions, management wishes to establish new production facilities (Optional Source), close to demand points in Europe. There are six potential locations (HUDTG, CZMCT, IEILG, FIMPF, PLZCA) for establishing a new production facility. Consequently, the product flow within TGE's supply chain is reconfigured as follows:
<img width="493" alt="image" src="https://github.com/user-attachments/assets/f4c5bfc0-4202-41f9-be0c-d2c06c02edfa" />

However, apart from variable production costs, these locations are associated with significant opening and operating costs, but they are expected to reduce transportation costs. Therefore, by considering location decisions your task is to reformulate the transhipment problem developed in Scenario 1 and to investigate the feasibility of opening a production facility.

## Scenario 3:
Recognizing that air freight is both expensive and environmentally unsustainable, TGE is proactively investigating alternative strategies to minimize costs and reduce its carbon footprint. Consequently, the management seeks to understand the impact of adopting an alternative transportation mode, encompassing sea freight and road in addition to air freight. It's important to note that the road transportation option is not available for the movement of goods from manufacturers to cross-docks; the only available options are air and sea freight. Although the cost factor plays a key role in the decision-making, the speed of the chosen transportation mode is also crucial for the company. TGE has analyzed historical data and discovered that different transportation modes are associated with different additional costs per unit distance, primarily attributable to variations in their transport speed. These additional costs encompass expenses incurred due to stockouts, backorders, penalty costs, and other factors. Internally, TGE refers to this category of cost as “slowness cost (𝜋),” and it is estimated for each transportation mode as follows:

• 𝜋 𝑎𝑖𝑟 = 0.00063 € 𝑢𝑛𝑖𝑡/𝑘𝑚

• 𝜋 𝑠𝑒𝑎 = 0.0521 € 𝑢𝑛𝑖𝑡/𝑘𝑚

• 𝜋 𝑟𝑜𝑎𝑑 = 0.00240 € 𝑢𝑛𝑖𝑡/𝑘𝑚

And now, TGE's management wishes to exert more effort into abating its carbon emissions. Please provide suggestions to TGE to make a trade-off between reducing its emissions compared to the current plans (Scenario 1 & 2) and the change in optimizing its allocation plan with a primary focus on minimizing the cost associated with carbon emissions. What is the effect of this new consideration on the allocation plan?

<img width="511" alt="image" src="https://github.com/user-attachments/assets/b60e74c3-a32e-40d8-a14f-bb8a4e29bfbe" />



