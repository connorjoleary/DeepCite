### Grab all
```
Map(
    Paginate(Match(Index("all_test"))),
    Lambda(x => q.Get(x))
)
```

### Grab most recent
```
CreateIndex({
  name: "all_school_queries",
  source: Collection('<yourcollection>'),
  values:   values: [
     {
       field: ["ts"]
     },
     {
       field: ["ref"]
     }
  ]
})

client.query(
    q.Map(
        q.Paginate(
    q.Match(q.Index("all_school_queries_by_ts")),

            {size:1000}
        ),
        q.Lambda(
            ["ts", "ref"],       // we now have two parameters
            q.Get(q.Var("ref"))  // and only use the ref, but the result will be automatically sorted by ts
        )
    )
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
