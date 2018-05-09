# Modeling Austin's Public Transit System

## Objective
Build a __Genetic Algorithm__ modeling class that can be used to design optimized bus transit routes for Austin's public transportation system with the purpose of attracting more riders and relieving road congestion.

## Background
City governments and researchers have been studying different ways to design efficient and useful transportation networks for over a century. Industry calls it the __Transit Network Design Problem__ and it aims to optimize across many objectives with a large potential solution space. Non-linear problems like this one have seen success using a Genetic Algorithm approach.

In the City of Austin, Capital Metro ridership rates have seen steady declines in their fixed route services. At this moment, the City of Austin is in the final stages of approving a new strategic mobility plan: [2025 Austin Metropolitan Area Transportation Plan](http://austintexas.gov/asmp "2025 AMATP"). In addition, Capital Metro has their own [Connections 2025](http://connections2025.org/ "Connections 2025") which is their answer to building a better connected transit system over the next 5-10 years. The current proposal by the City of Austin and Capital Metro appears well thought out and is excellently presented for public adoption. However, I have not been able to ascertain the scientific or data-driven techniques they used in creating their plan.

  * [Connections 2025 Fact Sheet](http://connections2025.org/wp-content/uploads/2016/01/Connections2025-factSheet-final-eng.pdf "Connections 2025 Facts")
  * [Market & Service Fact Sheet](http://connections2025.org/wp-content/uploads/2016/05/Connections2025_factsheet.pdf "Fact Sheet")

The [Downtown Alliance](http://www.downtownaustin.com/daa/transportation) also has a good web page for referencing all the major organizations involved in transportation and mobility for the City of Austin.

In researching this problem I found several scientific studies. Below is an example of one methodology used in India.  

* [Optimal Route Network Design For Transit Systems Using Genetic Algorithms](http://home.iitk.ac.in/~partha/eng-opt02): In this 2002 paper, the author uses a three step iterative process.
    1. Initial Route Set Generation (IRSG) with a pre-specified number of routes. Each route is determined by first selecting a starting node, then selecting all other nodes sequentially until either (i) the number of nodes reaches a maximum number, or (ii) the route length reaches a maximum.
    2. Evaluation of Route Set: A set of 'route goodness' metrics are determined and a single 'route goodness' score is calculated.
    3. Route Modification: utilizes a genetic algorithm to iterate over the routes in search for a better 'route goodness' score.

This [Stanford study](http://cs229.stanford.edu/proj2013/HuangLing-OptimizingPublicTransit.pdf "Optimizing Public Transit") uses a linear Regression model, and data from 25 U.S. cities to predict optimal station locations based on estimated ridership.

I also found this [Master Thesis](https://oatd.org/oatd/record?record=handle%5C%3A11427%5C%2F13368) from the University of Cape Town that looked into different heuristic algorithms and settled on using a Genetic Algorithm.


## Approach
My thesis is that the current bus route network is not convenient or useful enough for a large portion of the population. My strategy is to design a layered system, one that links population regions together with rapid connections that is layered on top of many regional networks that exclusively serve one specific area.

My goal is to minimize travel time and maximize network reach. To do so, I will initialize a new set of bus stops using block-level [population](http://connections2025.org/wp-content/uploads/2016/02/CapMetro_2010PopEmp.pdf "Population & Employment Density") data from the 2010 census. Then, I will define my regions, arbitrarily decide on a good location for the rapid network transit station, and pick the number of routes to be used in the area. Then I will implement a RouteFinder class, that uses a genetic algorithm to search for optimal routing, taking into account distance between nodes.  

I believe this approach will be successful because other cities have seen success with this method. I used the example from [Curitiba, Brazil](https://www.slideshare.net/TheMissionGroup/a-market-focused-paradigm-for-public-transit-pt-3-designing-effective-transit-networks) in designing this strategy, since they are known in the transportation industry as a model city on this topic. My theory is that making a fast and well interconnected network will encourage daily commuters to choose public transit over driving.


## Impact
The class I am building may serve as a useful tool for Capital Metro and the City of Austin in planning future mobility.

## Format
My class will be build in a python file and demonstrated in a JupyerNotebook.

## Data Sources
Austin Texas 2010 Census TIGER/Line Shapefiles downloaded from the [Census Bureau](https://www.census.gov/geo/maps-data/data/tiger-line.html)

## Next Steps
* Re-Define the fitness function to take into account the multiple paths a vehicle can traverse to get from one node to the next.
* Use an a-star graph search and weigh the edges (or paths) by average traffic flow speed.
* evaluate the full dataset on a remote server with a high number of random selections and evolutions
* Further enrich population data with jobs data

## Video
[Project Motivation and Progress](https://www.youtube.com/watch?v=HPuYPlqDluk&index=8&list=PLxtztEze-DRedrinVPfmde2jq9UKwxBzq)
