import random
import datetime as dt

BDS_id = list(range(1, 17))
up_time = ["2020-08-07", "2020-09-07"]
title = ["Bán nhà tại p.Phạm Ngũ Lão, Quận 1, 25m2", "Chung cư Opal Boulevard 95.49m² 3PN", "Bán nhà Phú Lãm. 34m*4T. tặng 3 điều hòa"]
poster_temp = ["môi giới", "VinHome", "SunHouse", "TTT", "PhuongMinh"]
area_temp = ["TpHCM", "HaNoi", "ThanhHoa", "NhaTrang"]
unit_temp = ["Tỷ"]
price_temp = list(range(1, 20))
per_unit_price = 3000.0
def generate_order() -> dict:
    random_bds_id = random.choice(BDS_id)
    random_time = random.choice(up_time)
    random_title = random.choice(title)
    random_poster_temp = random.choice(poster_temp)
    random_area_temp = random.choice(area_temp)
    random_price_temp = random.choice(price_temp)

    return {
        'BDS_id': random_bds_id,
        'time': random_time,
        'title': random_title,
        'poster_temp': random_poster_temp,
        'area_temp': random_area_temp,
        'unit_temp': 'Tỷ',
        'price_temp': random_price_temp,
        'final_price': random_price_temp * per_unit_price
        # 'created_at': dt.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
    }
