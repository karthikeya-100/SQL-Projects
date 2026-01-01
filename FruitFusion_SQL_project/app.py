import streamlit as st

st.set_page_config(layout="wide")

st.title("🍎 Fruit Dataset: SQL Analysis Portfolio")
st.markdown("This dashboard showcases SQL queries and their business applications for fruit inventory and health analytics.")
st.divider()

# --- ANALYTIC SECTION 1 ---
st.subheader("Which fruits have a shelf life below the overall average, and what is their sugar content?")

query1 = """
SELECT fruit_name, shelf_life_days, sugar_g 
FROM fruits_dataset 
WHERE shelf_life_days < (SELECT AVG(shelf_life_days) FROM fruits_dataset)
ORDER BY sugar_g DESC;
"""

col1, col2 = st.columns([2, 2])
with col1:
    st.code(query1)
with col2:
    with st.expander("🛠 SQL Technique & Justification"):
        st.write("**Technique:** Scalar Subquery in the WHERE clause.")
        st.write("**Business Value:** Helps inventory managers identify fruits that need fast turnover (due to low "
                 "shelf life) and plan their inventory.")


st.divider()

st.subheader("Calculate the count of fruits available in each season. Which season has the lowest variety?")
query2 = '''
    SELECT
season,COUNT(distinct fruit_name) as fruit_count
FROM fruits_dataset
GROUP BY season
ORDER BY 
CASE
	WHEN season = 'All' THEN 1 ELSE 0
END,
fruit_count desc;
'''
col1,col2 = st.columns([2,2])
with col1:
    st.code(query2)
with col2:
    with st.expander("🛠 SQL Technique & Justification"):
        st.write("**Technique:** Group by clause and using custom sorting using CASE statement.")
        st.write("**Business Value:** Helps procurement teams plan for off-season cost spikes and supply gaps.")

st.divider()

st.subheader("Find fruits that are in the bottom 25% for sugar content but top 25% for fiber content.")
query3 = '''
    with ranked as (
select *,
ntile(4) over (order by sugar_g) as sugar_q ,
ntile(4) over (order by fiber_g_per_100g desc) as fiber_q
from fruits_dataset
)
select fruit_name,sugar_g,fiber_g_per_100g from ranked where sugar_q = 1 and fiber_q = 1;
'''
col1,col2 = st.columns([2,2])
with col1:
    st.code(query3)
with col2:
    with st.expander("🛠 SQL Technique & Justification"):
        st.write("**Technique:** NTILE is used to divide dataset into 4 equal distributions. for sugar, ntile "
                 "identifies bottom 25% of rows which has low sugar. for fiber, ntile identifies top 25% of rows "
                 "which has high fiber. CTE is used to store this ranking and filtering this table to get actual output")
        st.write("**Business Value:** Provides targeted recommendations for health-conscious or diabetic customers.")


st.divider()
st.subheader("What is the average weight and water content of fruits categorized by their Taste Profile?")
query4 = '''
    select taste_profile,avg(avg_weight_g) as avg_weight,avg(water_percent) as avg_water_pct from fruits_dataset
group by taste_profile
order by avg_weight desc,avg_water_pct desc;
'''
col1,col2 = st.columns([2,2])
with col1:
    st.code(query4)
with col2:
    with st.expander("🛠 SQL Technique & Justification"):
        st.write("**Technique:** Group by Clause")
        st.write("**Business Value:** Provides information about which fruits are fleshy and watery to plan "
                 "and optimize transportation costs.")

st.divider()
st.subheader("Which are the top 3 longest-lasting fruits for each season?")

query5 = '''
with shelf_ranked as(
select fruit_name,season,shelf_life_days,
row_number() over(partition by season order by shelf_life_days desc) as shelf_rank
from fruits_dataset
)
select * from shelf_ranked where shelf_rank in (1,2,3);
'''
col1,col2 = st.columns([2,2])
with col1:
    st.code(query5)
with col2:
    with st.expander("🛠 SQL Technique & Justification"):
        st.write("**Technique:** Used partition by clause to divide fruits within each season. Used row number to "
                 "assign unique number for all fruits within each season. Filtering only top 3 rows from each "
                 "season.row_number doesnt care about ties hence we get exactly three rows per each season.")
        st.write("**Business Value:** Provides information about which fruits are long lasting which helps in plan "
                 "logistics.")

st.divider()

st.subheader("Which fruits provide Calcium or Iron as their predominant mineral but have a Sweet taste profile?")
query6 = '''
select * from fruits_dataset 
where top_mineral in ('Calcium','Iron') 
and taste_profile = 'Sweet';
'''
col1,col2 = st.columns([2,2])
with col1:
    st.code(query6)
with col2:
    with st.expander("🛠 SQL Technique & Justification"):
        st.write("**Technique:**.Used simple in operator and AND condition")
        st.write("**Business Value:** Finding sweet fruits with rare minerals allows seller to sell at premium cost.")


st.divider()
st.subheader("find which Predominant Vitamin appears in the most fruits vs. the least.")
query7 = '''
select top_vitamin,count(*) as vitamin_count from fruits_dataset
group by top_vitamin
order by vitamin_count desc;
'''
col1,col2 = st.columns([2,2])
with col1:
    st.code(query7)
with col2:
    with st.expander("🛠 SQL Technique & Justification"):
        st.write("**Technique:**.Used group by clause")
        st.write("**Business Value:** Provides information about which vitamin is most common in all fruits. "
                 "It helps health apps to recomment fruits based on vitamin deficiency")

st.divider()

st.subheader("List the top 5 fruits with the highest Water Content percentage that are available in Summer.")
query8 = '''
select * from fruits_dataset 
where season = 'Summer'
 order by water_percent desc limit 5;
'''
col1,col2 = st.columns([2,2])
with col1:
    st.code(query8)
with col2:
    with st.expander("🛠 SQL Technique & Justification"):
        st.write("**Technique:**.Used where and limit clause")
        st.write("**Business Value:** Provides information about fruits with high water content so that"
                 "businesses sell these fruits especially in summer to promote hydration")

st.divider()

st.subheader("Categorize fruits into three groups based on water content: 'High' (>90%), 'Medium' (80-90%), and 'Low' (<80%)"
             " What is the average calorie count for each of these three groups?")
query9 = '''
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
'''
col1,col2 = st.columns([2,2])
with col1:
    st.code(query9)
with col2:
    with st.expander("🛠 SQL Technique & Justification"):
        st.write("**Technique:**.Used Case when statement to create groups and used CTE to store this as a result."
                 "Used group by clause in outer query to find average calorie count for each group")
        st.write("**Business Value:** Helps businesses in marketing . for example, fruits with low calories and high "
                 "in water can be marketed to weight loss markets and fruits with high calories and low in water are "
                 "more in energy dense and can be marketed to athletes group")
st.divider()

st.subheader("Find fruits where the pH is extremely low (highly acidic) but the Sugar content is extremely high.")

query10 = '''
with outlier_ranked as
(
select *,
ntile(4) over(order by acidity_pH) as acidity_q,
ntile(4) over(order by sugar_g desc) as sugar_q
from fruits_dataset
)
select * from outlier_ranked 
where acidity_q = 1 and sugar_q = 1;
'''
col1,col2 = st.columns([2,2])
with col1:
    st.code(query10)
with col2:
    with st.expander("🛠 SQL Technique & Justification"):
        st.write("**Technique:**.ntile divides dataset into 4 parts. ntile gives value '1' for top 25% of rows"
                 "for acidity_ph column and gives value 1 for top 25% of rows for sugar_g column in descending order."
                 "Outer query used to fetch fruits with high acidity(low PH) and high sugar content")
        st.write("**Business Value:** These fruits have rare sweet-tart taste which might be outliers in some of "
                 "predictive models")

st.divider()




st.divider()
st.info("💡 Tip: Click the expander buttons on the right to view the technical breakdown of each analysis.")
