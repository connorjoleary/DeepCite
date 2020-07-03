CREATE table deepcite_retrieval(
    id UUID NOT NULL DEFAULT uuid_generate_v1(),
    user_id text,
    deepcite_call_id UUID NOT NULL,
    stage text,
    status_code integer,
    response_time_elapsed integer,
    current_versions jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT id_deepcite_retrieval PRIMARY KEY ( id ),
	FOREIGN KEY (deepcite_call_id) REFERENCES deepcite_retrieval (id)
);
