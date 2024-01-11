CREATE DATABASE IF NOT EXISTS sales_db;

USE sales_db;

CREATE TABLE area (
  area_temp VARCHAR(200),
  price_range VARCHAR(20),
  property_count INT
);

CREATE TABLE sales (
  BDS_id INT,
  time DATE,
  title VARCHAR(200),
  poster_temp VARCHAR(200),
  area_temp VARCHAR(100),
  unit_temp VARCHAR(10),
  price_temp FLOAT,
  final_price FLOAT
);

INSERT INTO sales (BDS_id, time, title, poster_temp, area_temp, unit_temp, price_temp, final_price)
VALUES
  (7, '2020-08-07', 'Bán nhà tại p.Phạm Ngũ Lão, Quận 1, 25m2, 4.2 TỶ', 'môi giới', 'PhuQuoc', 'tỷ', 4.2, 42000),
  (8, '2020-08-07', 'Chung cư Opal Boulevard 95.49m² 3PN', 'môi giới', 'PhuQuoc', 'tỷ', 3.308559, 33085),
  (10, '2020-08-07', 'Bán nhà Phú Lãm. 34m*4T. tặng 3 điều hòa, 1,62 tỷ', 'môi giới', 'DaNang', 'tỷ', 1.62, 16200),
  (12, '2020-08-07', 'Nhà trệt lầu . Hùynh thúc kháng', 'môi giới', 'CanTho', 'tỷ', 1.84, 18400),
  (14, '2020-08-07', 'Đất Lê Văn Lương, 85m2, Sổ riêng, Hẻm xe hơi, XDTD', 'môi giới', 'PhuQuoc', 'tỷ', 2.25, 22500),
  (15, '2020-08-07', 'Bán nhà Huyện Hóc Môn 34m²', 'phương minh', 'PhuQuoc', 'tỷ', 2.2, 22000),
  (16, '2020-08-07', 'Nhà 1 lửng 2PN đất 63m2 cực đẹp ĐS 17 Linh Trung', 'nhà đất đức ngân - mua bán nhà đất sài gòn', 'PhuQuoc', 'tỷ', 3.35, 33500);

INSERT INTO area (area_temp, price_range, property_count)
VALUES
    ('HaNoi', 'High', 4);