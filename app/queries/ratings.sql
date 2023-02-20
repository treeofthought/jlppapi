select
  b.title as "Title",
  b.author as "Author",
  round(avg(rating), 1) as "Avg",
  max(case when u.name = 'C' then r.rating else NULL end) as "C",
  max(case when u.name = 'D' then r.rating else NULL end) as "D",
  max(case when u.name = 'G' then r.rating else NULL end) as "G",
  max(case when u.name = 'J' then r.rating else NULL end) as "J",
  max(case when u.name = 'P' then r.rating else NULL end) as "P",
  max(case when u.name = 'S' then r.rating else NULL end) as "S"
from ratings r 
join books b on b.id = r.book_id
join users u on u.id = r.user_id
group by 1,2
order by avg(rating) desc, 2,1
