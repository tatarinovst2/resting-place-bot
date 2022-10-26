DROP TABLE IF EXISTS visited;
DROP TABLE IF EXISTS favorite;
DROP TABLE IF EXISTS ratedByUser;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS places;

CREATE TABLE places(
  id             SERIAL PRIMARY KEY,
  name           VARCHAR(100) NOT NULL,
  type           VARCHAR(10) NOT NULL,
  average_price  VARCHAR(200),
  address        VARCHAR(300),
  webpage        VARCHAR(200),
  working_hours  VARCHAR(200),
  phone_number   VARCHAR(100)
);

INSERT INTO places(id,name,type,average_price,address,webpage,working_hours,phone_number)
VALUES (1,
        'KFC',
        'Ресторан',
        '350',
        'Нижний Новгород, пр. Ленина, 33, 5-ый этаж',
        'https://kfc.ru',
        'С 9:00 до 21:00',
        NULL);
