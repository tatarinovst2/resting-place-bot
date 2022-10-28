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

CREATE TABLE visited(
  visited_id  SERIAL PRIMARY KEY,
  place_id INTEGER NOT NULL REFERENCES places(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL,
  is_visited BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE favorite(
  favorite_id  SERIAL PRIMARY KEY,
  place_id INTEGER NOT NULL REFERENCES places(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL,
  is_in_favorite BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE ratings(
    rating_id SERIAL PRIMARY KEY,
    place_id INTEGER NOT NULL UNIQUE REFERENCES places(id) ON DELETE CASCADE,
    one_stars INTEGER NOT NULL DEFAULT 0,
    two_stars INTEGER NOT NULL DEFAULT 0,
    three_stars INTEGER NOT NULL DEFAULT 0,
    four_stars INTEGER NOT NULL DEFAULT 0,
    five_stars INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE ratedByUser(
    rated_by_user_id SERIAL PRIMARY KEY,
    place_id INTEGER NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL
);

INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Сыроварня им. Аркадия Новикова','Ресторан','1700','Нижний Новгород, пл. Октябрьская, 1','https://www.syrovarnya.com/','Пн, Вт, Ср, Чт, Вс, с 08.00 до 23.59; Пт, Сб, с 08.00 до 03.00','7(831)215-19-19');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Mitrich','Ресторан','2000','Нижний Новгород, Ковалихинская, 8','http://mitrichsteakhouse.ru/','Пн - Вс с 11:00 до 00:00','7 (831) 282-82-10');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Yale','Ресторан','2000','Нижний Новгород, ул. Рождественская, 30','http://yalerestaurant.ru/?yandex-source=desktop-maps','Пн, Вт, Ср, Чт с 14:00 до 00:00; Пт, Сб, Вс с 12:00 до 00:00','7 (831) 215-01-51');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Mukka','Ресторан','1700','Нижний Новгород, ул. Ошарская, 36Б','http://ekproject.ru/mukka','Пн - Вс с 11:00 до 00:00','7 (831) 211-93-58');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Bottega Bistro','Ресторан','1500','Нижний Новгород,ул. Пискунова, 18А','https://bottegabistro.ru/','Пн - Вс с 10:00 до 23:00','7 (987) 086-11-00');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Парк Культуры','Ресторан','3000','Нижний Новгород, Верхне-Волжская наб., 10А','https://park-k.ru/','Пн - Вс с 9:00 до 00:00','7 (831) 424-47-07');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Red Wall','Ресторан','2000','Нижний Новгород, Кожевенная ул., 2','https://www.redwallrestaurant.ru/','Пн, Вт, Ср, Чт, Вс, с 10:00 до 00:00; Пт, Сб, с 10:00 до 02:00','7 (903) 060-62-26');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Юла Пицца','Ресторан','1000','Нижний Новгород, Октябрьская ул., 9Б','https://yulapizza.vsite.biz/','Пн, Вт, Ср, Чт, с 12:00 до 22:00; Пт, Сб, с 12:00 до 00:00; Вс с 12:00 до 23:00','7 (920) 299-06-96');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Пяткин','Ресторан','1300','Нижний Новгород, Рождественская ул., 25','https://pyatkinrest.ru/','Пн - Вс с 12:00 до 00:00','7 (831) 430-91-83');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Кусто','Ресторан','1500','Нижний Новгород, ул. Пискунова, 16','https://custo.rest/','Пн, Вт, Ср, Чт, Вс, с 12:00 до 00:00; Пт, Сб, с 12:00 до 01:00','7 (958) 835-85-15');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Ribs','Ресторан','2500','Нижний Новгород, ул. Белинского, 61','https://ribs-nn.ru/','Пн - Вс с 12:00 до 00:00','7 (831) 211-97-03');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Магадан','Ресторан','2500','Нижний Новгород, Октябрьская площадь, 1','https://www.novikovgroup.ru/restaurants/detail/magadan-nizhniy-novgorod/','Пн, Вт, Ср, Чт, Вс, с 12:00 до 00:00; Пт, Сб, с 12:00 до 04:00','7 (831) 215-20-20');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Экспедиция','Ресторан','3500','Нижний Новгород, Рождественская ул., 1','http://expedition-nn.ru/','Пн - Вс с 12:00 до 00:00','7 (831) 282-09-11');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Bocconcino','Ресторан','1500','Нижний Новгород, Алексеевская ул., 10/16','https://nn.bocconcino.ru/','Пн - Вс с 10:00 до 23:00','7 (831) 211-96-71');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Медные трубы','Бар','2500','Нижний Новгород, Рождественская ул., 40',NULL,'Ср, Чт, Вс с 18:00 до 02:00; Пт, Сб с 18:00 до 03:00; Пн, Вт - выходной','7 (929) 046-47-50');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Селедка&кофе','Бар','1500','Нижний Новгород, Рождественская ул., 19',NULL,'Пн, Вт, Ср, Чт, Вс, с 09:00 до 00:00; Пт, Сб, с 09:00 до 02:00','7 (831) 282-01-11');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Union Jack','Бар','2000','Нижний Новгород, Рождественская ул., 8','https://unionjack.ru/grandmusicpub/','Круглосуточно','7 (831) 414-17-34');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Skuratov','Кофейня','400','Нижний Новгород, Большая Покровская ул., 2','https://skuratovcoffee.ru/nn','Пн - Вс с 6:45 до 23:05','7 (999) 139-34-05');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Surf Coffee','Кофейня','400','Нижний Новгород, Большая Покровская ул., 51А,','https://www.surfcoffee.ru/','Пн - Пт с 08:00 до 22:00; Сб, Вс с 10:00 до 22:00','7 (987) 531-73-63');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Jeffrey''s Coffeeshop','Кофейня','400','Нижний Новгород, Большая Покровская ул., 82','https://jeffreys.ru/','Пн - Вс с 10:00 до 22:00','7 (929) 042-89-23');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Авиатор','Бар','3000','Нижний Новгород, Верхне-Волжская наб., 2Б',NULL,'Ср, Чт, Вс с 17:00 до 01:00; Пт, Сб с 17:00 до 02:00; Пн, Вт - выходной','7 (930) 206-07-57');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Нижегородский государственный академический театр драмы им. М. Горького','Театр','600','г. Нижний Новгород, ул. Большая Покровская, дом 13','https://drama.nnov.ru/','Пн-Вс с 10:00 до 20:00','7 (831) 419-51-73');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Нижегородский государственный академический театр оперы и балета имени А. С. Пушкин','Театр','1200','Нижний Новгород ул. Белинского, 59','https://operann.ru/','Пн-Вс с 9.30 до 19.00 с 14.00 до 14.30 обед','7 (831) 234-05-34');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Театр юного зрителя','Театр','400','ул. Максима Горького, 145, Нижний Новгород','https://tyuz.ru/#','Пн-вс с 10.00 до 19.00 перерыв на обед: с 14.15 до 15.00','7 (831) 428-31-25');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Комедия','Театр','600','ул. Грузинская, 23, Нижний Новгород','https://comedy.nnov.ru/','Пн-Вс с 10:00 до 20:00. Обеденный перерыв с 14:20 до 15:00','7 (831) 434-04-24');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Театр "Преображение"','Театр','450','ул. Июльских Дней 21/96','https://preo.su/','Пн. выходной. Ср. 17:30 — 18:30. Сб. 17:00 — 18:00. Вс. 10:00 — 11:00 и 15:00 — 16:00.','7 (831) 245-12-54, 7 (904) 398-71-50');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Нижегородский государственный академический театр кукол','Театр','300','г. Н. Новгород, ул. Б. Покровская, д. 39','http://www.ngatk.ru/','Пн-Вс с 10:00 до 18:30','7 (831) 434-09-22');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Усадьба С. М. Рукавишникова','Музей','взрослый билет: 250; льготный билет 170','Нижний Новгород, Верхне-Волжская наб., д.7','https://ngiamz.ru/filialy/usadba-rukavishnikovykh','Вт, ср, чт с 11:00 до 18:00; Пт, сб, вс c 11:00 до 18:00','7 (831) 282-25-47 (экскурсионный отдел); 7 (831) 282-25-46 (касса)');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Нижегородский государственный художественный музей (русская и советская живопись)','Музей','150 - 300','Нижний Новгород, Кремль, корпус 3; Нижний Новгород, Верхневолжская набережная, 3; Нижний Новгород, Площадь Минина и Пожарского, 2/2; Нижний Новгород, Кремль, корпус 1А','https://www.artmuseumnn.ru/','Вт.-Ср. с 10.00 до 18.00, Чт. с 12.00 до 20.00, в Пт.,Сб.,Вс с 11.00 до 19.00. Пн. - выходной день.','7 (910) 130-02-84, 7 (950) 351-38-32');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Музей А.М.Горького','Музей','Входной билет: 0 - 1710; Экскурсия: 400 - 1000','г. Нижний Новгород, ул. Семашко, 19','http://www.museumgorkogo.ru/muzej-kvartira-a-m-gorkogo','Понедельник, четверг - выходные дни Музей открыт с 9.00 до 17.00 Касса работает до 16.30 Технический перерыв в экспозиции: с 13.00 до 14.00','7 (831) 436-16-51');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Технический музей','Музей','150 - 350','Большая Покровская ул., 43 (3 этаж), Нижний Новгород','https://ngiamz.ru/filialy/tekhnicheskij-muzej','Вт - Вс  11:00-18:00 Пн, последний Чт месяца - музей закрыт.','7 (831) 215-10-60');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Государственный Русский музей фотографии','Музей','Полный билет (для граждан РФ): 150 руб. Полный билет (для граждан иностранных государств): 150 руб. Льготный билет (студенты-очники, школьники, пенсионеры): 75 руб.','г.Нижний Новгород, ул.Пискунова, 9а','https://www.fotomuseum.nnov.ru/','Пн. выходной день Вт-Вс с 11:00 до 19:00 Касса заканчивает работать за час до закрытия музея!','7 (831)411-82-47');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Музей истории художественных промыслов Нижегородской области','Музей','Входной билет: 80 - 150; Экскурсия: 250 - 700','Нижний Новгород, ул. Большая Покровская, д. 43, 4 этаж','https://ngiamz.ru/filialy/muzej-istorii-khudozhestvennykh-promyslov','Вт - Вс  11:00-18:00   Пн, последний Чт месяца - музей закрыт. (касса закрывается за 40 мин до окончания рабочего дня). Понедельник – выходной. Последний четверг месяца – санитарный день.','7 (831) 282-25-43');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Домик Каширина','Музей','Входной билет: 0 - 1710; Экскурсия: 400 - 1000','г. Нижний Новгород, Почтовый съезд, 21','http://museumgorkogo.ru/muzej-detstva-a-m-gorkogo-domik-kashirina','Вторник, среда - выходные дни Музей открыт с 9.00 до 17.00 (касса - до 16.30) Праздничные дни: с 11.00 до 19.00 (касса - до 18.30)','7 (831) 433-85-89');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Нижегородский Кремль','Музей','100 - 1800','Нижний Новгород, Кремль, 6а (Дмитриевская башня)','https://ngiamz.ru/filialy/nizhegorodskij-kreml','Пн-Вс с 10-00 до 18-00, кассы работают с 10-00 до 17-00 в Дмитриевской и Ивановской башнях','7 (831) 282-25-40');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('"Кварки" музей занимательных наук','Музей','https://kvarky.ru/stoimost-biletov.html','ул. Фильченкова, 10, ЦУМ, новое здание, 3 этаж.','https://kvarky.ru/','Пн-Вс с 11:00 до 18:00','7 (831) 423-42-51');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Арсенал. Центр современного искусства','Музей','100 - 400','Нижний Новгород, Кремль, корпус 6','https://arsenal-museum.art/','Пн — выходной Вт-Вс — 12:00–20:00 Касса до 19:00','7 (831) 422 45 54');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Парк чудес Галилео','Музей','https://nn.galileopark.ru/price/','Нижний Новгород, Казанское шоссе, 11, 3 этаж (ТРК "Индиго-Life")','https://nn.galileopark.ru/','Пн-Вс с 10:00 до 20:00 касса работает до 19:00','7 (831) 235-01-27');
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Империя Грёз','Кинотеатр',NULL,'Нижний Новгород, просп. Гагарина, 98; Нижний Новгород, Б.Покровская, 82, ТРК «Небо»; Нижний Новгород, Коминтерна, 105; Нижний Новгород, ул. Героя Смирнова, 14, 1 этаж (касса), 2 этаж (зал) Нижний Новгород, Казанское ш., 11, ТРК «Индиго Life»;','https://xn--c1adbibb0aykc7n.xn--p1ai/',NULL, NULL);
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Синима Парк','Кинотеатр',NULL,'Нижний Новгород, ул. Бетанкура, 1, ТРЦ «Седьмое небо», 1-й этаж; Нижний Новгород, ул. Родионова, 187в, ТРЦ «Фантастика», 3-й этаж','https://kinoteatr.ru/kinoafisha/nizhniy-novgorod/',NULL, NULL);
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Орлёнок','Кинотеатр',NULL,'Нижний Новгород, Б.Покровская, 39А','http://orlenok-kino.ru/',NULL,NULL);
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Стадион НН','Стадион','500 — 2 500','ул. Бетанкура, д. 1А','https://nn.kassir.ru/sport/stadion-nijniy-novgorod-2/fk-pari-nijniy-novgorod---fk-spartak_2022-10-02','2 октября 19:00',NULL);
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('ЦЕХ','Фестиваль','300-500','Нижполиграф, ул. Варварская, 32','https://intervalsfest.com/map/','12:00-23.00',NULL);
INSERT INTO places(name,type,average_price,address,webpage,working_hours,phone_number) VALUES ('Супер Дискотека','Концерт','1 200 — 2 800','пр-т Гагарина, 29','https://nn.kassir.ru/koncert/superdiskoteka-90-yih','21 октября 19:00',NULL);


INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (1,0,0,0,1,9);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (2,0,0,0,1,9);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (3,0,0,0,2,8);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (4,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (5,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (6,0,0,0,1,9);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (7,0,0,0,1,9);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (8,0,0,0,1,9);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (9,0,0,0,0,10);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (10,0,0,0,1,9);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (11,0,0,0,5,5);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (12,0,0,0,4,6);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (13,0,0,0,2,8);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (14,0,0,0,4,6);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (15,0,0,0,0,10);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (16,0,0,0,6,4);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (17,0,0,0,7,3);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (18,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (19,0,0,0,5,5);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (20,0,0,0,7,3);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (21,0,0,0,0,10);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (22,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (23,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (24,0,0,0,4,6);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (25,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (26,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (27,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (28,0,0,0,2,8);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (29,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (30,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (31,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (32,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (33,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (34,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (35,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (36,0,0,0,4,6);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (37,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (38,0,0,0,3,7);
INSERT INTO ratings(place_id,one_stars,two_stars,three_stars,four_stars,five_stars) VALUES (41,0,0,0,3,7);

