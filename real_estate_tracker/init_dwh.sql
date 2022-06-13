CREATE TABLE IF NOT EXISTS real_estate_facts (
	id SERIAL PRIMARY KEY,
	url VARCHAR(255) NOT NULL,
	ad_id VARCHAR(20) NOT NULL,
	city_id INTEGER NOT NULL,
	price INTEGER NOT NULL,
	price_per_sm INTEGER NOT NULL,
	area NUMERIC(6,2) NOT NULL,
	terrain_area INTEGER NOT NULL,
	build_year SMALLINT NOT NULL,
	market_type SMALLINT NOT NULL,
	number_of_rooms SMALLINT NOT NULL,
	date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS city_dimension (
	id SERIAL PRIMARY KEY,
	city VARCHAR(50) NOT NULL,
	region VARCHAR(50) NOT NULL,
	province VARCHAR(50) NOT NULL
);

ALTER TABLE real_estate_facts
    ADD CONSTRAINT fk_re_city FOREIGN KEY (city_id) REFERENCES city_dimension (id);
