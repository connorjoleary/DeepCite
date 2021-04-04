CREATE table source_label(
    id UUID NOT NULL DEFAULT uuid_generate_v1(),
    user_id text,
    base_id UUID NOT NULL,
    source_id UUID NOT NULL,
    stage text,
    current_versions jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT id_source_label PRIMARY KEY ( id ),
	FOREIGN KEY (base_id) REFERENCES deepcite_retrieval (id)
);
