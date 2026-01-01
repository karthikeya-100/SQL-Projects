select * from fruits_dataset;

# Question1
---------------------------------------------------------------------------------------------------------
# Which fruits have a shelf life below the overall average, and what is their  sugar content?
select fruit_name,shelf_life_days,sugar_g from fruits_dataset where shelf_life_days <
(select round(avg(shelf_life_days),2) as average_shelf_life from fruits_dataset)
order by sugar_g desc;
# Business now know about which fruits has lower shelf life and their sugar content which helps in controlling inventory

#Question2
-------------------------------------------------------------------------------------------------------------
# Calculate the count of fruits available in each season. Which season has the lowest variety?
select
season,count(distinct fruit_name) as fruit_count
from fruits_dataset
group by season
order by 
case
	when season = 'All' then 1 else 0
end,
fruit_count desc;
# Business now know about number of varieties available in each season, helps them plan off season cost spike

# Question 3
-------------------------------------------------------------------------------------------
# Find fruits that are in the bottom 25% for sugar content but top 25% for fiber content.
with ranked as (
select *,
ntile(4) over (order by sugar_g) as sugar_q ,
ntile(4) over (order by fiber_g_per_100g desc) as fiber_q
from fruits_dataset
)
select fruit_name,sugar_g,fiber_g_per_100g from ranked where sugar_q = 1 and fiber_q = 1;
# These fruits have low in sugar and high in fiber, perfect recommendation for diabetic

# Question 4
-----------------------------------------------------------------------------------------------------
# What is the average weight and water content of fruits categorized by their "Taste Profile"?
select taste_profile,avg(avg_weight_g) as avg_weight,avg(water_percent) as avg_water_pct from fruits_dataset
group by taste_profile
order by avg_weight desc,avg_water_pct desc;

# fruits with sweet taste have avg weight of 559 and water percentage of 81% which means these fruits are heavy and fleshy
# which makes high transportation cost 

# Juicer is percentage of water content
# easier to process as it is watery to extract juice
# less solid waste

# Question5
----------------------------------------------------------------------------------------------------------
# Within each Season, rank the fruits by their Shelf Life from longest to shortest. 
# Which are the top 3 longest-lasting fruits for each season?
with shelf_ranked as(
select fruit_name,season,shelf_life_days,
row_number() over(partition by season order by shelf_life_days desc) as shelf_rank
from fruits_dataset
)
select * from shelf_ranked where shelf_rank in (1,2,3);
# This helps business to plan logistics properly

# Question 6
---------------------------------------------------------------------------------------------------------
# Which fruits provide "Calcium" or "Iron" as their predominant mineral but have a "Sweet" taste profile?
select * from fruits_dataset where top_mineral in ('Calcium','Iron') and taste_profile = 'Sweet';
# finding sweet fruits with high in rare minerals allows retailer to sell at premium cost

# Question 7
-------------------------------------------------------------------------------------------------------------
# find which "Predominant Vitamin" appears in the most fruits vs. the least.
select top_vitamin,count(*) as vitamin_count from fruits_dataset
group by top_vitamin
order by vitamin_count desc;
# Hels health apps businesses to recomment fruits based on users vitamin deficiencies

# Question 8
-----------------------------------------------------------------------------------------------------------
# List the top 5 fruits with the highest Water Content percentage that are available in "Summer."
select * from fruits_dataset 
where season = 'Summer'
 order by water_percent desc limit 5;
# Helps businesses to sell these fruits in summer has hydration is needed

# Question 9
-------------------------------------------------------------------------------------------------------------------
#Categorize fruits into three groups based on water content: 'High' (>90%), 'Medium' (80-90%), and 'Low' (<80%).
# What is the average calorie count for each of these three groups?
with categories as
(
select *,
case 
	when water_percent > 90 then 'High'
    when water_percent between 80 and 90 then 'Medium'
    else 'Low'
end as 'Water_content_group'
from fruits_dataset
)
select Water_content_group,round(avg(calories),2) 
from categories
group by Water_content_group;
select * from fruits_dataset;

#"Find fruits where the pH is extremely low (highly acidic) but the Sugar content is extremely high." 
# This identifies unique "Sweet-Tart" flavor profiles that might be outliers in a predictive model.
with outlier_ranked as
(
select *,
ntile(4) over(order by acidity_pH) as acidity_q,
ntile(4) over(order by sugar_g desc) as sugar_q
from fruits_dataset
)
select * from outlier_ranked where acidity_q = 1 and sugar_q = 1;
