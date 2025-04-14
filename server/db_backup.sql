PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('b21934d1faa6');
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	password_hash VARCHAR NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (username)
);
CREATE TABLE saved_locations (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	location_name VARCHAR NOT NULL, 
	latitude FLOAT, 
	longitude FLOAT, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE search_records (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	"query" VARCHAR NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE search_records_locations (
	search_record_id INTEGER NOT NULL, 
	saved_location_id INTEGER NOT NULL, 
	PRIMARY KEY (search_record_id, saved_location_id), 
	FOREIGN KEY(saved_location_id) REFERENCES saved_locations (id), 
	FOREIGN KEY(search_record_id) REFERENCES search_records (id)
);
CREATE TABLE weather_data (
	id INTEGER NOT NULL, 
	location_id INTEGER NOT NULL, 
	current_temperature FLOAT NOT NULL, 
	current_humidity FLOAT NOT NULL, 
	current_wind_speed FLOAT NOT NULL, 
	weather_condition VARCHAR(50) NOT NULL, 
	forecast_data JSON NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(location_id) REFERENCES saved_locations (id)
);
COMMIT;
