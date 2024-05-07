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
  fund_id
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
  SELECT
    custom_field_id,
    values,
    portfolio_investment_id
  FROM `vestberry-demo-warehouse.aws_lambda.custom_field_values`
  LEFT JOIN (
    SELECT
      id,
      name
    FROM `vestberry-demo-warehouse.aws_lambda.custom_field_definitions`
  ) ON id = custom_field_id
  WHERE name='Program'
)

SELECT * FROM p_summary LEFT JOIN p_investment USING(portfolio_investment_id) LEFT JOIN rounds USING(portfolio_investment_id) LEFT JOIN fund USING(fund_id) 
LEFT JOIN (SELECT values AS program, portfolio_investment_id FROM custom_fields) USING(portfolio_investment_id)