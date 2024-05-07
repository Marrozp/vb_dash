WITH p_summary AS(
SELECT
  cut_of_date,
  portfolio_investment_id,
  first_check_mo_ic,
  irr,
  multiple,
  ownership,
  total_original_cost,
  proceeds,
  cash_realized,
  current_share_value,
  total_return,
  fund_id,
  latest_investment_stage
FROM `vestberry-demo-warehouse.aws_lambda.portfolio_summary`),
p_investment AS (
SELECT
  id AS portfolio_investment_id,
  display_name,
  domicile_country,
  entry_round,
  industries
FROM `vestberry-demo-warehouse.aws_lambda.portfolio_investment`),
fund AS (
SELECT
  id AS fund_id,
  display_name AS fund_name
FROM `vestberry-demo-warehouse.aws_lambda.fund`),
rounds AS (
  SELECT
    portfolio_investment_id,
    AVG(round_size) OVER (PARTITION BY portfolio_investment_id) AS round_size,
    AVG(pre_money) OVER (PARTITION BY portfolio_investment_id) AS pre_money,
    AVG(post_money) OVER (PARTITION BY portfolio_investment_id) AS post_money
  FROM `vestberry-demo-warehouse.aws_lambda.financing_round`),
custom_fields AS (
  SELECT portfolio_investment_id, MAX(program) AS program, MAX(female_founder) AS female_founder, MAX(board_seat) AS board_seat, MAX(source_of_introduction) AS source_of_introduction, MAX(deal_lead) AS deal_lead FROM (
    SELECT
      custom_field_id,
      values,
      portfolio_investment_id,
      LOWER(REGEXP_REPLACE(name, ' ', '_')) AS name
    FROM `vestberry-demo-warehouse.aws_lambda.custom_field_values`
    LEFT JOIN (
      SELECT
        id,
        name
      FROM `vestberry-demo-warehouse.aws_lambda.custom_field_definitions`
    ) ON id = custom_field_id
    WHERE name='Program' OR name='Female founder' OR name='Board seat' OR name='Source of introduction' OR name='Deal Lead'
  ) PIVOT (MAX(values) FOR name IN('program','female_founder','board_seat','source_of_introduction','deal_lead')) GROUP BY portfolio_investment_id
)

SELECT * FROM p_summary LEFT JOIN p_investment USING(portfolio_investment_id) LEFT JOIN rounds USING(portfolio_investment_id) LEFT JOIN fund USING(fund_id) 
LEFT JOIN (
  SELECT 
    program, 
    female_founder,
    board_seat,
    source_of_introduction,
    deal_lead,
    portfolio_investment_id 
FROM custom_fields) USING(portfolio_investment_id)