CREATE table deepcite_call(
    id UUID NOT NULL DEFAULT uuid_generate_v1(),
    user_id text,
    stage text,
    status_code integer,
    response jsonb,
    response_time_elapsed integer,
    current_versions jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT id_tbl PRIMARY KEY ( id )
);
