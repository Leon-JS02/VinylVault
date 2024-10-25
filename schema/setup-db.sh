psql postgres -c "DROP DATABASE IF EXISTS vinylvault;"
psql postgres -c "CREATE DATABASE vinylvault;"
psql postgres -f schema.sql