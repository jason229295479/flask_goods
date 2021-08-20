# register  blue print


def register(app):
    # need import your view  example user
    from controller.user import login_bp, users_bp, user, users, login
    from controller.sms import sms_bp, sms
    from controller.access_records import record_bps, records
    from controller.inventory_management import goods_bp, goods_category_bp, goods
    app.register_blueprint(sms_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(record_bps)
    app.register_blueprint(goods_bp)
    app.register_blueprint(goods_category_bp)
