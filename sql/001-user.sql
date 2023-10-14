CREATE TABLE IF NOT EXISTS users (
    id           uuid PRIMARY KEY         NOT NULL DEFAULT uuid_generate_v4(),
    email        text NOT NULL,
    phone        text,
    status       text                     NOT NULL,
    level        text                     NOT NULL,
    logged_in_at timestamp WITH TIME ZONE,
    created_at   timestamp WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at   timestamp WITH TIME ZONE,
    deleted_at   timestamp WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS index_users_by_email
    ON users(email) WHERE deleted_at IS NULL;

CREATE TRIGGER trigger_user_updated_at
    BEFORE UPDATE
    ON users
    FOR EACH ROW
EXECUTE PROCEDURE update_updated_at();
