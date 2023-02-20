with bottom_five as (
  select
    r.book_id,
    round(avg(r.rating), 1) as avg,
    rank() over (order by avg(r.rating) asc, b.author, b.title)
  from ratings r 
  join books b on b.id = r.book_id
  group by 1, b.author, b.title
  order by 2 desc 
)

select
  b.title as "Title",
  b.author as "Author",
  bf.avg as "Avg",
  max(case when u.name = 'C' then r.rating else NULL end) as "C",
  max(case when u.name = 'D' then r.rating else NULL end) as "D",
  max(case when u.name = 'G' then r.rating else NULL end) as "G",
  max(case when u.name = 'J' then r.rating else NULL end) as "J",
  max(case when u.name = 'P' then r.rating else NULL end) as "P",
  max(case when u.name = 'S' then r.rating else NULL end) as "S"
from bottom_five bf
join ratings r on r.book_id = bf.book_id
join users u on u.id = r.user_id
join books b on b.id = bf.book_id
where bf.rank <= 5
group by 1,2,3, bf.book_id, bf.rank
order by bf.rank
