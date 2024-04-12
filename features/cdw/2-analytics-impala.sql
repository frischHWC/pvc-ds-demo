USE datagen_finance;

-- Who is the trader who bought the most actions ? -- 
SELECT t.name, t.id, count(*) as number_of_transactions, SUM(p.volume) as volume_of_actions
FROM stock_price_transaction p
RIGHT OUTER JOIN traders t ON (t.id = p.trader_id)
WHERE p.buy_or_sell = 'BUY'
GROUP BY t.id, t.name
ORDER BY volume_of_actions DESC
;
