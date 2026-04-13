from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Auction, Product


PRODUCTS = [
    {'brand': 'Nike', 'name': "Air Force 1 '07", 'category': 'nike', 'price': 110, 'resell_price': 145, 'badge': 'Classic', 'image_url': 'https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/e6da41fa-1be4-4ce5-b89c-22be4f1f02d4/air-force-1-07-shoes-WrLlWX.png'},
    {'brand': 'Nike', 'name': 'Dunk Low Retro', 'category': 'nike', 'price': 110, 'resell_price': 190, 'badge': 'HOT', 'image_url': 'https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/8409c3b2-add4-4b18-927f-2767435a660b/dunk-low-retro-shoes-Zc0601.png'},
    {'brand': 'Air Jordan', 'name': 'AJ1 Low SE', 'category': 'jordan', 'price': 120, 'resell_price': 210, 'badge': 'Trending', 'image_url': 'https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/07f289b9-7ca1-49ec-a347-b69b95e17032/air-jordan-1-low-se-shoes-H7DD5v.png'},
    {'brand': 'Air Jordan', 'name': 'AJ1 Retro High OG', 'category': 'jordan', 'price': 180, 'resell_price': 340, 'badge': 'HOT', 'image_url': 'https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/03ac93ba-0ab0-4e37-a623-9972de262234/air-jordan-1-retro-high-og-shoes-Pz6fZ9.png'},
    {'brand': 'Nike', 'name': 'Air Max 97', 'category': 'nike', 'price': 175, 'resell_price': 220, 'badge': 'Limited', 'image_url': 'https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/b212e5bf-ec2f-4b0d-b759-37e893003043/air-max-97-shoes-EBZrb8.png'},
    {'brand': 'Nike', 'name': 'Air Max 90 GTX', 'category': 'nike', 'price': 145, 'resell_price': 165, 'badge': 'New', 'image_url': 'https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/d4abdad5-4e03-4e34-a790-cb2bbd06e4c2/air-max-90-gore-tex-shoes-K3mBRb.png'},
    {'brand': 'Air Jordan', 'name': 'Jordan Stadium 90', 'category': 'jordan', 'price': 130, 'resell_price': 175, 'badge': 'New', 'image_url': 'https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/00166372-1221-4ff0-92ee-f8d990044fdf/jordan-stadium-90-shoes-Jn6ZH4.png'},
    {'brand': 'Nike', 'name': 'Dunk Low Classic', 'category': 'nike', 'price': 110, 'resell_price': 155, 'badge': 'Classic', 'image_url': 'https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/07874320-fba8-4712-8670-34df66141622/dunk-low-shoes-T4Ckpv.png'},
]


def seed_initial_data(db: Session) -> None:
    if db.query(Product).count() == 0:
        db.add_all(Product(**item) for item in PRODUCTS)

    if db.query(Auction).count() == 0:
        now = datetime.utcnow()
        db.add_all([
            Auction(name='Air Jordan 38 PF Basketball', image_url='https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/99d0eb30-f290-4b37-a124-51ccd23c6d1c/air-jordan-xxxviii-pf-basketball-shoes-tTRwfF.png', current_bid=285, ends_at=now + timedelta(hours=2)),
            Auction(name='Nike LeBron NXXT Gen EP', image_url='https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/74e02a76-fe86-48e0-bd76-2993548666a3/lebron-nxxt-gen-ep-basketball-shoes-bkxBVS.png', current_bid=195, ends_at=now + timedelta(hours=1)),
            Auction(name='Nike Freak 5 EP Basketball', image_url='https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/30927f64-1c21-4475-a730-5c48e931d1b7/freak-5-ep-basketball-shoes-dPwdt7.png', current_bid=145, ends_at=now + timedelta(hours=3)),
        ])

    db.commit()
