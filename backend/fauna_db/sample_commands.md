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
  name: "most_recent_calls",
  source: Collection('deepcite_call'),
  values: [
     {
       field: ["ts"], reverse: true
     },
     {
       field: ["ref"]
     }
  ]
})

client.query(
    q.map_(
        q.lambda_(
            ["ts", "ref"],       
            q.get(q.var("ref")) 
        ),
        q.paginate(
            q.match(q.index("most_recent_calls"))
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

### Create string of source, link, and versions from all entries
`CreateIndex({ name: "all_deepcite_call", source: Collection("deepcite_call") })`

```
Map(Paginate(Match(Index('all_deepcite_call')), { size: 30 }),
  Lambda(
    'call',
    Concat(
        [
            Select(['data', 'response', 'results', 0, 'source'], Get(Var('call')), ''),
            Select(['data', 'response', 'results', 0, 'link'], Get(Var('call')), ''),
            Select(['data', 'current_versions', 'api'], Get(Var('call')), ''),
            Select(['data', 'current_versions', 'model'], Get(Var('call')), ''),
            Select(['data', 'current_versions', 'lambda'], Get(Var('call')), ''),
            Select(['data', 'current_versions', 'extension'], Get(Var('call')), '')
        ]
    )
  )
)
```