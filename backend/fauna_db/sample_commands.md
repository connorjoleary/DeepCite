### Grab all
```
Map(
    Paginate(Match(Index("all_test"))),
    Lambda(x => q.Get(x))
)
```
### Count values by field
```
CreateIndex({
  name: "deepcite_calls_user",
  source: Collection("deepcite_call"),
  values: [{ field: ["data", "user_id"] }]
})

CreateIndex({
  name: "deepcite_calls_by_user",
  source: Collection("deepcite_call"),
  terms: [{ field: ["data", "user_id"] }]
})

Let(
  {
    user_id: Distinct(Paginate(Match(Index("deepcite_calls_user"))))
  },
  Map(
    Var("user_id"),
    Lambda(
      "user_id",
      Let(
        {
          refs: Match(Index("deepcite_calls_by_user"), Var("user_id"))
        },
        {
          user_id: Var("user_id"),
          total: Count(Var("refs"))
        }
      )
    )
  )
)
```
