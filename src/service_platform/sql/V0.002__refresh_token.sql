CREATE TABLE refresh_tokens
(
    id         UUID                     NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id    UUID                     NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL             DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TRIGGER trigger_refresh_token_updated_at
    BEFORE UPDATE
    ON refresh_tokens
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at();
