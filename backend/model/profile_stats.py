import pstats
p = pstats.Stats('profile')
p.sort_stats('cumulative').print_stats('backend/model/')