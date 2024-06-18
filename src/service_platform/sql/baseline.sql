-- Drop all rows in schema_version table
TRUNCATE TABLE schema_version;

-- Insert a new row for baseline
INSERT INTO schema_version (installed_rank,
                            version,
                            description,
                            type,
                            script,
                            checksum,
                            installed_by,
                            execution_time,
                            success)
VALUES (1, '000', '<< Flyway Baseline >>', 'BASELINE', '<< Flyway Baseline >>', NULL,
        'null', 0, TRUE);
