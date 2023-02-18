with top_five as (
  select
    book_id,
    round(avg(rating)) as avg,
    rank() over (order by avg(rating) desc)
  from ratings
  group by 1
  order by 2 desc 
)

select
  b.title as "Title",
  b.author as "Author",
  tf.avg as "Avg",
  max(case when u.name = 'C' then r.rating else NULL end) as "C",
  max(case when u.name = 'D' then r.rating else NULL end) as "D",
  max(case when u.name = 'G' then r.rating else NULL end) as "G",
  max(case when u.name = 'J' then r.rating else NULL end) as "J",
  max(case when u.name = 'P' then r.rating else NULL end) as "P",
  max(case when u.name = 'S' then r.rating else NULL end) as "S"
from top_five tf
join ratings r on r.book_id = tf.book_id
join users u on u.id = r.user_id
join books b on b.id = tf.book_id
where tf.rank <= 5
group by 1,2,3, tf.book_id, tf.rank
order by tf.rank
