ALTER table source_label
add column "redact" BOOLEAN DEFAULT FALSE
COMMENT "If true the user has taken back this being the source.";