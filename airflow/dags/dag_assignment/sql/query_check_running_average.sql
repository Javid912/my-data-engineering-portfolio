SELECT *,
  avg(Quantity) OVER(ORDER BY InvoiceDate
     ROWS BETWEEN 2 PRECEDING AND CURRENT ROW )
     as moving_average
from retail.raw_invoices