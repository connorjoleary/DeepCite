### Grab all
Map(
    Paginate(Match(Index("all_test"))),
    Lambda(x => q.Get(x))
)